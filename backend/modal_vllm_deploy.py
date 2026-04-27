"""
Modal vLLM Deployment — Qwen 2.5 7B Instruct (OpenAI-compatible API).

Deploy:
    modal deploy backend/modal_vllm_deploy.py

Usage after deploy:
    export VLLM_ENDPOINT="https://your-app--vllm-qwen.modal.run"
    export VLLM_API_KEY="sk-local"  # vLLM doesn't require a real key

Cost: ~$1.10/hr on A10G (Modelo cabe en ~14 GB VRAM).
      ~$0.055 por post de blog con pipeline completo.

GPU options (edit below):
    - A10G  (24 GB, ~$1.10/hr) — recomendado, margen de sobra
    - L4    (24 GB, ~$0.80/hr) — más barato, misma VRAM, ~30% más lento
    - T4    (16 GB, ~$0.60/hr) — justo para 7B con AWQ/INT4
"""

import modal
from modal import Image, App, Secret, asgi_app

# ── Configuration ──────────────────────────────────────────────
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
GPU_TYPE = "A10G"            # A10G | L4 | T4
GPU_COUNT = 1
MAX_MODEL_LEN = 8192         # Contexto máximo (tokens)
CONTAINER_IDLE_TIMEOUT = 300  # 5 min sin requests → scale to zero

# ── vLLM image ─────────────────────────────────────────────────
vllm_image = (
    Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm>=0.6.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "transformers>=4.44.0",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

app = App("vllm-qwen25-7b")


@app.cls(
    image=vllm_image,
    gpu=f"{GPU_TYPE}:{GPU_COUNT}",
    secrets=[Secret.from_name("huggingface-secret")],
    scaledown_window=CONTAINER_IDLE_TIMEOUT,
)
@modal.concurrent(max_inputs=10)
class VLLMQwen:
    """vLLM server with Qwen 2.5 7B, OpenAI-compatible API."""

    @modal.enter()
    def load_model(self):
        import os
        from vllm.engine.arg_utils import AsyncEngineArgs
        from vllm.engine.async_llm_engine import AsyncLLMEngine
        from vllm.entrypoints.openai.serving_chat import OpenAIServingChat
        from vllm.entrypoints.openai.serving_completion import OpenAIServingCompletion
        from vllm.entrypoints.openai.protocol import (
            ChatCompletionRequest, CompletionRequest, ErrorResponse,
        )
        from vllm.entrypoints.openai.serving_engine import BaseModelPath

        # Use HuggingFace token for gated model access
        hf_token = os.environ.get("HF_TOKEN", os.environ.get("HUGGINGFACE_TOKEN"))
        
        engine_args = AsyncEngineArgs(
            model=MODEL_ID,
            tokenizer=MODEL_ID,
            tensor_parallel_size=GPU_COUNT,
            max_model_len=MAX_MODEL_LEN,
            gpu_memory_utilization=0.92,
            enforce_eager=False,  # Use CUDA graphs for speed
            enable_prefix_caching=True,
        )

        self.engine = AsyncLLMEngine.from_engine_args(engine_args)
        
        # Set up the OpenAI-compatible serving layers
        served_model = BaseModelPath(name=MODEL_ID.split("/")[-1], model_path=MODEL_ID)
        
        self.chat_serving = OpenAIServingChat(
            engine=self.engine,
            served_model_names=[served_model],
            response_role="assistant",
            lora_modules=[],
            prompt_adapters=[],
            chat_template=None,
        )
        
        self.completion_serving = OpenAIServingCompletion(
            engine=self.engine,
            served_model_names=[served_model],
            lora_modules=[],
            prompt_adapters=[],
        )

    @asgi_app()
    def serve(self):
        """OpenAI-compatible API endpoint."""
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
        from fastapi.middleware.cors import CORSMiddleware

        web_app = FastAPI(title="Qwen 2.5 7B — vLLM")
        
        web_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @web_app.get("/health")
        async def health():
            return {"status": "healthy", "model": MODEL_ID}

        @web_app.get("/v1/models")
        async def list_models():
            return {
                "object": "list",
                "data": [{"id": MODEL_ID.split("/")[-1], "object": "model"}],
            }

        @web_app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            body = await request.json()
            req = ChatCompletionRequest(**body)
            generator = await self.chat_serving.create_chat_completion(req, raw_request=request)
            
            if isinstance(generator, ErrorResponse):
                return JSONResponse(content=generator.model_dump(), status_code=generator.code)
            
            # Streaming or non-streaming
            if req.stream:
                from fastapi.responses import StreamingResponse
                return StreamingResponse(
                    self._stream_response(generator),
                    media_type="text/event-stream",
                )
            
            # Collect full response
            final = None
            async for chunk in generator:
                final = chunk
            return JSONResponse(content=final.model_dump() if final else {})

        @web_app.post("/v1/completions")
        async def completions(request: Request):
            body = await request.json()
            req = CompletionRequest(**body)
            generator = await self.completion_serving.create_completion(req, raw_request=request)
            
            if isinstance(generator, ErrorResponse):
                return JSONResponse(content=generator.model_dump(), status_code=generator.code)
            
            final = None
            async for chunk in generator:
                final = chunk
            return JSONResponse(content=final.model_dump() if final else {})

        return web_app

    async def _stream_response(self, generator):
        """Stream SSE chunks."""
        async for chunk in generator:
            yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"


@app.function(
    image=vllm_image,
    secrets=[Secret.from_name("huggingface-secret")],
)
def test_locally(prompt: str = "Explica qué es la computación cuántica en 2 frases."):
    """Quick test: call the deployed endpoint from Modal."""
    import requests
    import os
    
    # When running inside Modal, get the web URL
    endpoint = os.environ.get("VLLM_ENDPOINT", "http://localhost:8000")
    
    resp = requests.post(
        f"{endpoint}/v1/chat/completions",
        json={
            "model": MODEL_ID.split("/")[-1],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 200,
        },
        timeout=60,
    )
    return resp.json()

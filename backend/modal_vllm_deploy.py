"""
Modal vLLM Deployment — Qwen 2.5 7B Instruct (OpenAI-compatible API).

Deploy:
    modal deploy backend/modal_vllm_deploy.py

Usage:
    export VLLM_ENDPOINT="https://alejandrors21--vllm-qwen25-7b-vllmqwen-serve.modal.run"

Cost: ~$1.10/hr on A10G (14 GB VRAM).
"""

import modal
from modal import Image, App, Secret, asgi_app

# ── Configuration ──────────────────────────────────────────────
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
GPU_TYPE = "A10G"
GPU_COUNT = 1
MAX_MODEL_LEN = 8192
CONTAINER_IDLE_TIMEOUT = 300

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
    """Qwen 2.5 7B via vLLM AsyncEngine, OpenAI-compatible API."""

    @modal.enter()
    async def load_model(self):
        """Load the model into GPU memory."""
        import os
        from vllm.engine.arg_utils import AsyncEngineArgs
        from vllm.engine.async_llm_engine import AsyncLLMEngine

        engine_args = AsyncEngineArgs(
            model=MODEL_ID,
            tokenizer=MODEL_ID,
            tensor_parallel_size=GPU_COUNT,
            max_model_len=MAX_MODEL_LEN,
            gpu_memory_utilization=0.92,
            enforce_eager=False,
            enable_prefix_caching=True,
        )

        self.engine = AsyncLLMEngine.from_engine_args(engine_args)
        self.model_name = MODEL_ID.split("/")[-1]

    @asgi_app()
    def serve(self):
        """OpenAI-compatible API endpoint."""
        import json
        import uuid
        import time
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse, StreamingResponse
        from fastapi.middleware.cors import CORSMiddleware
        from vllm import SamplingParams
        from vllm.utils import random_uuid

        web_app = FastAPI(title=f"Qwen 2.5 7B — vLLM")

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
                "data": [{"id": self.model_name, "object": "model"}],
            }

        @web_app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            body = await request.json()
            messages = body.get("messages", [])
            temperature = body.get("temperature", 0.7)
            max_tokens = body.get("max_tokens", 2000)

            # Convert messages to vLLM prompt format
            prompt = self._messages_to_prompt(messages)

            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95,
            )

            request_id = random_uuid()
            start_time = time.time()

            try:
                # Generate
                results_generator = self.engine.generate(
                    prompt=prompt,
                    sampling_params=sampling_params,
                    request_id=request_id,
                )

                final_output = None
                async for result in results_generator:
                    final_output = result

                if final_output is None or not final_output.outputs:
                    raise RuntimeError("Empty generation result")

                text = final_output.outputs[0].text
                finish_reason = "stop"
                usage = {
                    "prompt_tokens": len(final_output.prompt_token_ids),
                    "completion_tokens": len(final_output.outputs[0].token_ids),
                    "total_tokens": len(final_output.prompt_token_ids) + len(final_output.outputs[0].token_ids),
                }

                return JSONResponse(content={
                    "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": self.model_name,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": text,
                        },
                        "finish_reason": finish_reason,
                    }],
                    "usage": usage,
                })

            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": {"message": str(e), "type": "internal_error"}},
                )

        return web_app

    @staticmethod
    def _messages_to_prompt(messages: list) -> str:
        """Convert OpenAI-format messages to a prompt string for Qwen."""
        # Qwen 2.5 chat template
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt_parts.append(f"<|im_start|>system\n{content}<|im_end|>\n")
            elif role == "user":
                prompt_parts.append(f"<|im_start|>user\n{content}<|im_end|>\n")
            elif role == "assistant":
                prompt_parts.append(f"<|im_start|>assistant\n{content}<|im_end|>\n")
        prompt_parts.append("<|im_start|>assistant\n")
        return "".join(prompt_parts)


@app.function(
    image=vllm_image,
    secrets=[Secret.from_name("huggingface-secret")],
)
def test_locally(prompt: str = "Explica qué es la computación cuántica en 2 frases."):
    """Quick test: call the deployed endpoint."""
    import requests
    import os

    endpoint = os.environ.get("VLLM_ENDPOINT", "https://alejandrors21--vllm-qwen25-7b-vllmqwen-serve.modal.run")

    resp = requests.post(
        f"{endpoint}/v1/chat/completions",
        json={
            "model": "Qwen2.5-7B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 200,
        },
        timeout=120,
    )
    return resp.json()

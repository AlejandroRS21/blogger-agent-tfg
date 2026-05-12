import modal
import os

app = modal.App("blogger-agent-models")

# Define the model to use
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
MODEL_DIR = "/root/models"

def download_model():
    """Download the model weights from HuggingFace to bake into the Modal image."""
    from huggingface_hub import snapshot_download
    import os
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    snapshot_download(
        MODEL_NAME,
        local_dir=MODEL_DIR,
        ignore_patterns=["*.pt", "*.bin"],  # Use safetensors for faster loading
        token=os.environ.get("HF_TOKEN")
    )

# Create an image with vLLM and pre-downloaded weights
vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm",
        "huggingface_hub",
        "hf-transfer",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        download_model,
        secrets=[modal.Secret.from_name("huggingface-secret")]
    )
)

@app.cls(
    gpu="A10G",  # 24GB VRAM, enough for 7B models
    image=vllm_image,
    timeout=600,
    scaledown_window=120,
)
class LlamaModel:
    @modal.enter()
    def setup(self):
        import time
        from vllm import LLM
        print("Loading model weights into GPU...")
        start = time.time()
        
        # Load the model into vLLM
        self.llm = LLM(
            model=MODEL_DIR,
            tensor_parallel_size=1,
            trust_remote_code=True,
            max_model_len=4096, # Adjust if needed for longer contexts
        )
        self.tokenizer = self.llm.get_tokenizer()
        print(f"Model loaded in {time.time() - start:.2f}s")

    @modal.method()
    def generate(self, messages, temperature=0.7, max_tokens=2000):
        """
        Generate text matching OpenAI's ChatCompletion API shape internally.
        """
        from vllm import SamplingParams
        
        # Apply chat template
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        sampling_params = SamplingParams(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.95,
        )
        
        print("Generating response...")
        outputs = self.llm.generate([prompt], sampling_params)
        generated_text = outputs[0].outputs[0].text
        
        return {
            "content": generated_text.strip(),
            "model": MODEL_NAME,
            "finish_reason": "stop"
        }

# Local entrypoint for testing
@app.local_entrypoint()
def test_model():
    model = LlamaModel()
    response = model.generate.remote(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain what a webhook is in 2 sentences."}
        ],
        temperature=0.7,
        max_tokens=150
    )
    print("\n--- Response ---")
    print(response["content"])

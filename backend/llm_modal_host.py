"""
Modal script to host a Llama 3.1 model.
This provides the backend for the ModalProvider in the Blogger Agent.

Usage:
    modal run backend/llm_modal_host.py
    # or to deploy permanently:
    modal deploy backend/llm_modal_host.py
"""

import modal
import os
from typing import Dict, List, Any, Optional

# Define the Modal app
app = modal.App("blogger-agent-models")

# Define the container image
# We need torch and transformers for Llama
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "transformers>=4.44.0",
        "torch>=2.4.0",
        "accelerate>=0.33.0",
        "huggingface_hub>=0.24.0",
        "fastapi[standard]",  # Required for web endpoints
    )
)

@app.cls(
    image=image,
    gpu="A10G",  # Use an A10G GPU (24GB VRAM) - good for 7-8B models
    timeout=600,
    # secrets=[modal.Secret.from_name("huggingface-secret")],  # Optional if model is public
)
class LlamaModel:
    @modal.enter()
    def load_model(self):
        """Load the model into GPU memory when the container starts."""
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # Using Qwen 2.5 7B as it's highly capable and often doesn't require gated access
        model_id = "Qwen/Qwen2.5-7B-Instruct"
        print(f"Loading model: {model_id}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        
    @modal.method()
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """Generate a response using the model."""
        import torch
        
        # Qwen uses chatml-like format, apply_chat_template handles it
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            output_tokens = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
            
        # Get only the new tokens
        new_tokens = output_tokens[0][len(inputs["input_ids"][0]):]
        content = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        
        return {
            "content": content,
            "model": "qwen-2.5-7b-instruct",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": len(inputs["input_ids"][0]),
                "completion_tokens": len(new_tokens),
                "total_tokens": len(inputs["input_ids"][0]) + len(new_tokens),
            }
        }

@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
def api(data: Dict[str, Any]):
    """Optional web endpoint to call the model via HTTP."""
    model = LlamaModel()
    return model.generate.remote(
        messages=data.get("messages", []),
        temperature=data.get("temperature", 0.7),
        max_tokens=data.get("max_tokens", 1000),
    )

if __name__ == "__main__":
    # Test local execution of the Modal app logic (will download model locally)
    print("This script is intended to be run with 'modal run' or 'modal deploy'.")
    print("Example: modal run backend/llm_modal_host.py")

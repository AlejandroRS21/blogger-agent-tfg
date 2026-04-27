"""
VLLM Provider — Calls a vLLM server (OpenAI-compatible API) deployed on Modal.

Uses the OpenAI client pointed at a custom base_url.
Requires openai>=1.0.0 and the vLLM endpoint URL.
"""

from typing import List, Dict, Optional
import os
import logging

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base import LLMProvider, LLMResponse, LLMConfig

logger = logging.getLogger(__name__)


class VLLMProvider(LLMProvider):
    """
    Provider for a vLLM server (OpenAI-compatible API).
    
    Deployed on Modal with Qwen 2.5 7B Instruct.
    
    Environment variables:
        VLLM_ENDPOINT:  URL of the vLLM server (e.g., https://xxx--vllm-qwen.modal.run)
        VLLM_API_KEY:   API key (vLLM uses "sk-local" or any non-empty string by default)
    """
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Install with: pip install openai>=1.0.0")
        
        # Endpoint URL from config or env
        self.endpoint = os.getenv("VLLM_ENDPOINT", "").rstrip("/")
        if config.model and config.model.startswith("http"):
            self.endpoint = config.model  # Allow passing endpoint as model param
        
        if not self.endpoint:
            raise ValueError(
                "VLLM_ENDPOINT not set. Set the environment variable to your vLLM server URL.\n"
                "Deploy with: modal deploy backend/modal_vllm_deploy.py"
            )
        
        # API key (vLLM accepts any non-empty string by default)
        api_key = config.api_key or os.getenv("VLLM_API_KEY", "sk-local")
        
        # Model name for requests
        self.model_name = config.model or "Qwen2.5-7B-Instruct"
        
        # Create OpenAI client pointed at vLLM
        self.client = OpenAI(
            base_url=f"{self.endpoint}/v1",
            api_key=api_key,
        )
        
        self._available = True
    
    def is_available(self) -> bool:
        return self._available
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Create chat completion via vLLM."""
        if not self.is_available():
            raise RuntimeError("VLLM provider not available.")
        
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens if max_tokens is not None else self.config.max_tokens
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temp,
                max_tokens=tokens,
                timeout=120,
            )
            
            choice = response.choices[0]
            content = choice.message.content or ""
            finish_reason = choice.finish_reason or "stop"
            
            usage = {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            }
            
            return LLMResponse(
                content=content,
                model=self.model_name,
                provider="vllm",
                finish_reason=finish_reason,
                usage=usage,
            )
            
        except Exception as e:
            logger.error(f"vLLM API error: {e}")
            raise RuntimeError(f"vLLM API error (endpoint={self.endpoint}, model={self.model_name}): {e}")
    
    def create_messages(self, system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

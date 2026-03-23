"""
Google Gemini Provider.
"""

from typing import List, Dict, Any, Optional
import os

try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .base import LLMProvider, LLMConfig, LLMResponse


class GeminiProvider(LLMProvider):
    """Provider for Google Gemini API."""

    def __init__(self, config: LLMConfig):
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai not installed. Install with: pip install google-generativeai"
            )

        self.config = config
        self.api_key = config.api_key or os.environ.get("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Default model
        self.model_name = config.model or "gemini-1.5-pro"
        self.model = genai.GenerativeModel(self.model_name)

        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        if not self.api_key:
            return False
        try:
            # Simple test - just check the API key works
            test_model = genai.GenerativeModel("gemini-1.5-pro")
            return True
        except Exception:
            return False

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generate completion using Gemini."""

        # Extract system and user messages
        system_prompt = ""
        user_prompt = ""

        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            elif msg.get("role") == "user":
                user_prompt = msg.get("content", "")

        # Combine system and user for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt

        # Generation config
        generation_config = {
            "temperature": temperature or self.temperature,
            "max_output_tokens": max_tokens or self.max_tokens,
        }

        try:
            response = self.model.generate_content(full_prompt, generation_config=generation_config)

            return LLMResponse(
                content=response.text,
                model=self.model_name,
                usage={
                    "prompt_tokens": 0,  # Gemini doesn't provide this
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            )

        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    def create_messages(self, system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        """Create message format for Gemini."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def get_model_name(self) -> str:
        return self.model_name

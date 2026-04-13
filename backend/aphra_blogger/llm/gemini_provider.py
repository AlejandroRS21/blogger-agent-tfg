"""
Google Gemini provider implementation using the new google-genai SDK.
"""

from typing import List, Dict, Optional
import os
import logging

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .base import LLMProvider, LLMResponse, LLMConfig

logger = logging.getLogger(__name__)


def _is_gemini_model(model_id: str) -> bool:
    """Return True if model identifier looks like a Gemini model."""
    clean = model_id.strip().lower()
    return clean.startswith("gemini") or clean.startswith("models/gemini")


class GeminiProvider(LLMProvider):
    """Google Gemini API provider (google-genai)."""
    
    def __init__(self, config: LLMConfig):
        """Initialize Gemini provider."""
        super().__init__(config)
        
        if not GEMINI_AVAILABLE:
            raise ImportError("google-genai package not installed. Install with: pip install google-genai")
        
        # Priority: explicit config key -> GEMINI_API_KEY env -> GOOGLE_API_KEY env
        api_key = config.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if api_key:
            # Clean API key (remove quotes and spaces)
            api_key_clean = str(api_key).strip().strip('"').strip("'")
            
            try:
                self.client = genai.Client(api_key=api_key_clean)
                
                model_id = (config.model or "").strip()
                if not model_id:
                    self.model_id = "gemini-2.0-flash"
                elif _is_gemini_model(model_id):
                    self.model_id = model_id.replace("models/", "", 1)
                else:
                    raise ValueError(
                        f"Model '{model_id}' is incompatible with provider 'gemini'. "
                        "Use a Gemini model like 'gemini-1.5-flash'."
                    )

                # Keep a compatibility fallback chain across SDK/API versions.
                self.model_candidates = []
                for candidate in [
                    self.model_id,
                    "gemini-2.0-flash",
                    "gemini-1.5-flash-latest",
                    "gemini-flash-latest",
                    "gemini-1.5-pro-latest",
                ]:
                    if candidate not in self.model_candidates:
                        self.model_candidates.append(candidate)
            except ValueError:
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Gemini is available."""
        return self.client is not None
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Create completion with Gemini using google-genai SDK."""
        if not self.is_available():
            raise RuntimeError("Gemini client not initialized. Check API key.")
        
        # Separate system instruction from contents
        system_instruction = None
        contents = []
        
        for msg in messages:
            role = msg['role']
            content = msg.get('content', '')
            
            if role == 'system':
                system_instruction = content
            elif role == 'user':
                contents.append(types.Content(role='user', parts=[types.Part(text=content)]))
            elif role == 'assistant' or role == 'model':
                contents.append(types.Content(role='model', parts=[types.Part(text=content)]))
        
        if not contents:
             contents.append(types.Content(role='user', parts=[types.Part(text="Hello")]))

        try:
            response = None
            last_error = None
            for candidate in getattr(self, "model_candidates", [self.model_id]):
                try:
                    # Use generate_content from the new SDK
                    response = self.client.models.generate_content(
                        model=candidate,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            temperature=temperature if temperature is not None else self.config.temperature,
                            max_output_tokens=max_tokens if max_tokens is not None else self.config.max_tokens,
                            system_instruction=system_instruction,
                        )
                    )
                    self.model_id = candidate
                    break
                except Exception as candidate_error:
                    last_error = candidate_error
                    err_text = str(candidate_error).lower()
                    if "not found" in err_text or "404" in err_text:
                        continue
                    raise

            if response is None:
                raise RuntimeError(
                    f"No compatible Gemini model available. Tried: {getattr(self, 'model_candidates', [self.model_id])}. Last error: {last_error}"
                )
            
            # Extract text from response
            response_text = ""
            finish_reason = "STOP"
            
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                response_text = response.candidates[0].content.parts[0].text
                if hasattr(response.candidates[0], 'finish_reason'):
                    finish_reason = str(response.candidates[0].finish_reason)

            if not response_text:
                raise RuntimeError(
                    f"Gemini returned empty content for model {self.model_id}."
                )
            
            # Usage metadata
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }
            
            return LLMResponse(
                content=response_text,
                model=self.model_id,
                provider="gemini",
                finish_reason=finish_reason,
                usage=usage
            )
            
        except Exception as e:
            logger.error(f"Gemini API error with provider gemini and model {self.model_id}: {e}")
            raise RuntimeError(
                f"Gemini API error (provider=gemini, model={self.model_id}): {e}"
            )

    def create_messages(self, system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        """Create messages in OpenAI format for the provider."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

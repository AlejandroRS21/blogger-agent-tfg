"""
Factory for creating LLM providers.
"""

from typing import Optional
import os

from .base import LLMProvider, LLMConfig
from .openai_provider import OpenAIProvider
from .huggingface_provider import HuggingFaceProvider
from .modal_provider import ModalProvider
from .gemini_provider import GeminiProvider


def _default_model_for_provider(provider: str) -> str:
    """Return the default model for a provider."""
    defaults = {
        "openai": "gpt-4-turbo-preview",
        "huggingface": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "gemini": "gemini-2.0-flash",
        "modal": "blogger-agent-models/LlamaModel.generate",
        "auto": "gpt-4-turbo-preview",
    }
    return defaults.get(provider, defaults["auto"])


def _is_gemini_model(model: str) -> bool:
    """Check if a model identifier belongs to Gemini family."""
    clean = model.strip().lower()
    return clean.startswith("gemini") or clean.startswith("models/gemini")


def resolve_model_for_provider(provider: str, model: Optional[str]) -> str:
    """Resolve an effective model compatible with the selected provider."""
    if not model:
        return _default_model_for_provider(provider)

    clean_model = model.strip()

    if provider == "gemini":
        # Prevent cross-provider model leakage (e.g. meta-llama on Gemini).
        if _is_gemini_model(clean_model):
            return clean_model.replace("models/", "", 1)
        if "/" in clean_model:
            return _default_model_for_provider("gemini")
        return clean_model

    if provider == "huggingface" and _is_gemini_model(clean_model):
        return _default_model_for_provider("huggingface")

    return clean_model


def create_llm_provider(
    provider: str = "auto",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    **kwargs
) -> LLMProvider:
    """
    Create an LLM provider instance.
    
    Args:
        provider: Provider name ("openai", "huggingface", "gemini", "auto")
                 "auto" will try HuggingFace first, then OpenAI
        api_key: API key for the provider
        model: Model to use
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        **kwargs: Additional provider-specific config
        
    Returns:
        LLMProvider instance
        
    Raises:
        ValueError: If provider is invalid or not available
    """
    model = resolve_model_for_provider(provider, model)
    
    config = LLMConfig(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    
    # Auto mode: try Modal first if configured, then HuggingFace, then OpenAI
    if provider == "auto":
        # Check for Modal config
        modal_ready = (os.getenv("MODAL_TOKEN_ID") and os.getenv("MODAL_TOKEN_SECRET")) or os.getenv("MODAL_API_KEY")
        if modal_ready:
            try:
                modal_config = LLMConfig(
                    api_key=api_key or os.getenv("MODAL_API_KEY"),
                    model=resolve_model_for_provider("modal", model),
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = ModalProvider(modal_config)
                if llm.is_available():
                    return llm
            except Exception:
                pass

        # Check for Gemini token
        gemini_token = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_token:
            try:
                gemini_v_config = LLMConfig(
                    api_key=gemini_token,
                    model=resolve_model_for_provider("gemini", model),
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = GeminiProvider(gemini_v_config)
                if llm.is_available():
                    return llm
            except Exception:
                pass

        # Check for HF token
        hf_token = api_key or os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if hf_token:
            try:
                hf_config = LLMConfig(
                    api_key=hf_token,
                    model=resolve_model_for_provider("huggingface", model),
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = HuggingFaceProvider(hf_config)
                if llm.is_available():
                    return llm
            except Exception:
                pass
        
        raise ValueError(
            "No LLM provider available (Gemini, Modal or HuggingFace). OpenAI is disabled. "
            "Set GEMINI_API_KEY, MODAL_TOKEN_ID/SECRET or HF_TOKEN environment variable."
        )
    
    # Specific provider requested
    elif provider == "gemini":
        llm = GeminiProvider(config)
        if not llm.is_available():
            raise ValueError(
                "Gemini provider not available. "
                f"Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable. Effective model: {config.model}"
            )
        return llm

    elif provider == "huggingface":
        llm = HuggingFaceProvider(config)
        if not llm.is_available():
            raise ValueError(
                "HuggingFace provider not available. "
                "Set HF_TOKEN or HUGGINGFACE_TOKEN environment variable."
            )
        return llm
        
    elif provider == "modal":
        llm = ModalProvider(config)
        if not llm.is_available():
            raise ValueError(
                "Modal provider not available. "
                "Set MODAL_TOKEN_ID and MODAL_TOKEN_SECRET environment variables."
            )
        return llm
    
    elif provider == "openai":
        llm = OpenAIProvider(config)
        if not llm.is_available():
            raise ValueError(
                "OpenAI provider not available. Set OPENAI_API_KEY environment variable."
            )
        return llm
    
    else:
        raise ValueError(
            f"Unknown provider: {provider}. Valid options: 'openai', 'huggingface', 'gemini', 'auto'"
        )


def get_default_provider() -> LLMProvider:
    """
    Get the default LLM provider.
    
    Priority:
    1. HuggingFace (if HF_TOKEN set)
    2. OpenAI (if OPENAI_API_KEY set)
    
    Returns:
        LLMProvider instance
        
    Raises:
        ValueError: If no provider is available
    """
    return create_llm_provider(provider="auto")

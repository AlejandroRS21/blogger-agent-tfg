"""
Factory for creating LLM providers.
"""

from typing import Optional
import os

from .base import LLMProvider, LLMConfig
from .openai_provider import OpenAIProvider
from .huggingface_provider import HuggingFaceProvider
from .modal_provider import ModalProvider


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
        provider: Provider name ("openai", "huggingface", "auto")
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
    # Default model based on provider
    if model is None or "/" not in model:
        if provider == "openai":
            model = "gpt-4-turbo-preview"
        elif provider == "huggingface":
            model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        elif provider == "modal":
            # Default Modal function name
            model = "blogger-agent-models/LlamaModel.generate"
        else:  # auto
            model = "gpt-4-turbo-preview"  # Will be overridden per provider
    
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
                    model="blogger-agent-models/LlamaModel.generate",
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = ModalProvider(modal_config)
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
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
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
            "No LLM provider available (Modal or HuggingFace). OpenAI is disabled. "
            "Set MODAL_TOKEN_ID/SECRET or HF_TOKEN environment variable."
        )
    
    # Specific provider requested
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
            f"Unknown provider: {provider}. Valid options: 'openai', 'huggingface', 'auto'"
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

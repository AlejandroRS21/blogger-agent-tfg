"""
Factory for creating LLM providers.
"""

from typing import Optional
import os

from .base import LLMProvider, LLMConfig
from .openai_provider import OpenAIProvider
from .huggingface_provider import HuggingFaceProvider


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
    if model is None:
        if provider == "openai":
            model = "gpt-4-turbo-preview"
        elif provider == "huggingface":
            model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        else:  # auto
            model = "gpt-4-turbo-preview"  # Will be overridden per provider
    
    config = LLMConfig(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    
    # Auto mode: try HuggingFace first (free/cheaper), then OpenAI
    if provider == "auto":
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
                pass  # Fall through to OpenAI
        
        # Fall back to OpenAI
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        if openai_key:
            openai_config = LLMConfig(
                api_key=openai_key,
                model="gpt-4-turbo-preview",
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            llm = OpenAIProvider(openai_config)
            if llm.is_available():
                return llm
        
        raise ValueError(
            "No LLM provider available. Set HF_TOKEN or OPENAI_API_KEY environment variable."
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

"""
Factory for creating LLM providers.

Priority in "auto" mode:
  1. VLLM (Modal Qwen 2.5 7B) — cheapest self-hosted
  2. Gemini — free tier available
  3. HuggingFace — free Inference API
  4. OpenAI — disabled in auto (explicit only)
"""

from typing import Optional
import os

from .base import LLMProvider, LLMConfig
from .vllm_provider import VLLMProvider
from .openai_provider import OpenAIProvider
from .huggingface_provider import HuggingFaceProvider
from .gemini_provider import GeminiProvider
from .modal_provider import ModalProvider


def _default_model_for_provider(provider: str) -> str:
    """Return the default model for a provider."""
    defaults = {
        "vllm": "Qwen2.5-7B-Instruct",
        "openai": "gpt-4-turbo-preview",
        "huggingface": "Qwen/Qwen2.5-72B-Instruct",
        "gemini": "gemini-2.0-flash",
        "modal": "blogger-agent-models/LlamaModel.generate",
        "auto": "Qwen2.5-7B-Instruct",
    }
    return defaults.get(provider, defaults["auto"])


def resolve_model_for_provider(provider: str, model: Optional[str]) -> str:
    """Resolve an effective model compatible with the selected provider."""
    if not model:
        return _default_model_for_provider(provider)

    clean_model = model.strip()

    if provider == "gemini":
        if clean_model.lower().startswith("gemini") or clean_model.lower().startswith("models/gemini"):
            return clean_model.replace("models/", "", 1)
        if "/" in clean_model:
            return _default_model_for_provider("gemini")
        return clean_model

    if provider == "huggingface" and clean_model.lower().startswith("gemini"):
        return _default_model_for_provider("huggingface")

    if provider == "vllm" and clean_model.startswith("http"):
        return clean_model  # Allow passing endpoint URL as model

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
        provider: Provider name ("vllm", "openai", "huggingface", "gemini", "modal", "auto")
                 "auto" will try: VLLM → Gemini → HuggingFace
        api_key: API key for the provider
        model: Model to use (or endpoint URL for vllm)
        temperature: Sampling temperature (0.0-1.0)
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

    # ── Auto mode: try providers in priority order ──
    if provider == "auto":
        # 1. VLLM (cheapest self-hosted, deployed on Modal)
        vllm_endpoint = os.getenv("VLLM_ENDPOINT", "")
        if vllm_endpoint:
            try:
                vllm_config = LLMConfig(
                    api_key=api_key or os.getenv("VLLM_API_KEY", "sk-local"),
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = VLLMProvider(vllm_config)
                if llm.is_available():
                    return llm
            except Exception:
                pass

        # 2. Modal provider (Modal Function lookup)
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

        # 3. Gemini (free tier available)
        gemini_token = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_token:
            try:
                gemini_config = LLMConfig(
                    api_key=gemini_token,
                    model=resolve_model_for_provider("gemini", model),
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                llm = GeminiProvider(gemini_config)
                if llm.is_available():
                    return llm
            except Exception:
                pass

        # 4. HuggingFace (free Inference API)
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
            "No LLM provider available. Configure one of:\n"
            "  - VLLM:   set VLLM_ENDPOINT (Modal Qwen 2.5 7B)\n"
            "  - Gemini: set GEMINI_API_KEY (free tier)\n"
            "  - HF:     set HF_TOKEN (free Inference API)\n"
            "OpenAI requires explicit provider='openai'."
        )

    # ── Specific provider requested ──
    elif provider == "vllm":
        llm = VLLMProvider(config)
        if not llm.is_available():
            raise ValueError(
                "VLLM provider not available. Set VLLM_ENDPOINT environment variable.\n"
                "Deploy with: modal deploy backend/modal_vllm_deploy.py"
            )
        return llm

    elif provider == "gemini":
        llm = GeminiProvider(config)
        if not llm.is_available():
            raise ValueError(
                "Gemini provider not available. "
                f"Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
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
            f"Unknown provider: {provider}. "
            f"Valid options: 'vllm', 'openai', 'huggingface', 'gemini', 'modal', 'auto'"
        )


def get_default_provider() -> LLMProvider:
    """
    Get the default LLM provider with auto-detection.

    Priority: VLLM → Gemini → HuggingFace
    """
    return create_llm_provider(provider="auto")

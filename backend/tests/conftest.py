import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Ensure no real API keys are used during tests by stubbing them."""
    env_vars = {
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "MODAL_TOKEN_ID": "test-modal-id",
        "MODAL_TOKEN_SECRET": "test-modal-secret"
    }
    with patch.dict(os.environ, env_vars):
        yield

@pytest.fixture
def mock_llm_responses():
    """A dictionary fixture storing mock responses, customizable per test."""
    return {
        "openai_content": "Mocked OpenAI text: AI trends for 2026...",
        "anthropic_content": "Mocked Anthropic analysis: 4 headers, 10 paragraphs.",
    }

@pytest.fixture(autouse=True)
def apply_llm_mocks(mock_llm_responses):
    """Automatically mock both OpenAI and Anthropic SDK async creation calls."""
    
    # --- OpenAI ---
    mock_openai_message = MagicMock()
    mock_openai_message.content = mock_llm_responses["openai_content"]
    
    mock_openai_choice = MagicMock()
    mock_openai_choice.message = mock_openai_message
    
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [mock_openai_choice]
    
    async def async_openai_create(*args, **kwargs):
        return mock_openai_response

    # --- Anthropic ---
    mock_anthropic_content = MagicMock()
    mock_anthropic_content.text = mock_llm_responses["anthropic_content"]
    
    mock_anthropic_response = MagicMock()
    mock_anthropic_response.content = [mock_anthropic_content]

    async def async_anthropic_create(*args, **kwargs):
        return mock_anthropic_response

    # We patch assuming the codebase imports and instantiates the client locally.
    with patch("openai.resources.chat.completions.AsyncCompletions.create", new_callable=AsyncMock, side_effect=async_openai_create, create=True) as mock_oai,\
         patch("anthropic.resources.messages.AsyncMessages.create", new_callable=AsyncMock, side_effect=async_anthropic_create, create=True) as mock_anth:
        yield { "openai": mock_oai, "anthropic": mock_anth }

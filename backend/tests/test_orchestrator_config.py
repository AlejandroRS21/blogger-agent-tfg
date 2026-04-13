import pytest
import os
from unittest.mock import patch
from src.orchestrator.config import OrchestratorConfig

class TestOrchestratorConfigValidation:
    
    def test_validate_with_openai_key(self):
        """Should pass validation with OPENAI_API_KEY."""
        config = OrchestratorConfig(openai_api_key="sk-123")
        # Should not raise
        config.validate()

    def test_validate_with_hf_token(self):
        """Should pass validation with HF_TOKEN."""
        config = OrchestratorConfig(huggingface_token="hf-123")
        # Should not raise
        config.validate()

    def test_validate_with_gemini_key_only(self):
        """
        T001: Baseline test to reproduce validation failure with only Gemini key.
        NOTE: This test is expected to FAIL if the current code has the reported bug.
        """
        # Limpiamos el entorno para que no haya otras llaves que puedan interferir
        with patch.dict(os.environ, {}, clear=True):
            config = OrchestratorConfig(gemini_api_key="gemini-123")
            
            # Si el bug existe, validate() podría no reconocer gemini_api_key 
            # o lanzar un error que no la menciona.
            try:
                config.validate()
            except ValueError as e:
                # Si falla, verificamos si el mensaje de error menciona GEMINI
                error_msg = str(e)
                assert "GEMINI_API_KEY" in error_msg, f"Error message should mention GEMINI_API_KEY: {error_msg}"
                # Si llegamos aquí y falla el assert o lanza ValueError, T002 confirmará el fallo.
                raise e

    def test_validate_fails_with_no_keys(self):
        """Should raise ValueError when no keys are provided."""
        config = OrchestratorConfig()
        # Aseguramos que no hay nada en os.environ que valide
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as excinfo:
                config.validate()
            assert "At least one API key must be set" in str(excinfo.value)

    def test_validate_fails_for_selected_provider_without_key(self):
        """Should fail when provider is explicitly selected but credentials are missing."""
        with patch.dict(os.environ, {}, clear=True):
            config = OrchestratorConfig(provider="gemini")
            with pytest.raises(ValueError) as excinfo:
                config.validate()
            assert "Provider 'gemini' selected" in str(excinfo.value)

    def test_validate_empty_gemini_key_treated_as_missing(self):
        """Empty GEMINI_API_KEY must be considered missing."""
        with patch.dict(os.environ, {}, clear=True):
            config = OrchestratorConfig(gemini_api_key="   ", provider="gemini")
            with pytest.raises(ValueError) as excinfo:
                config.validate()
            assert "GEMINI_API_KEY" in str(excinfo.value)

    def test_validate_publish_interval_hours(self):
        """Continuous publishing interval must be positive."""
        config = OrchestratorConfig(openai_api_key="sk-123", publish_interval_hours=0)
        with pytest.raises(ValueError, match="publish_interval_hours"):
            config.validate()

    def test_validate_redundancy_threshold_range(self):
        """Redundancy threshold must stay in [0, 1]."""
        config = OrchestratorConfig(openai_api_key="sk-123", redundancy_threshold=1.2)
        with pytest.raises(ValueError, match="redundancy_threshold"):
            config.validate()

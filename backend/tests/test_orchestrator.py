"""Tests for the Blogger Orchestrator."""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig
from src.orchestrator.state import StateManager, WorkflowState, PhaseStatus
from aphra_blogger.llm.factory import resolve_model_for_provider
from aphra_blogger.llm.base import LLMConfig
from aphra_blogger.llm.gemini_provider import GeminiProvider, GEMINI_AVAILABLE


class TestOrchestratorConfig:
    """Tests for OrchestratorConfig."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = OrchestratorConfig.default()
        assert config.default_model == "gpt-4-turbo-preview"
        assert config.max_retries == 3
        assert config.verbose == True
    
    def test_config_validation_missing_keys(self):
        """Test validation fails without API keys."""
        with patch.dict(os.environ, {}, clear=True):
            config = OrchestratorConfig(
                openai_api_key=None,
                anthropic_api_key=None
            )
            with pytest.raises(ValueError, match="At least one API key"):
                config.validate()
    
    def test_config_validation_invalid_retries(self):
        """Test validation fails with negative retries."""
        config = OrchestratorConfig(
            openai_api_key="test-key",
            max_retries=-1
        )
        with pytest.raises(ValueError, match="max_retries"):
            config.validate()
    
    def test_config_to_dict(self):
        """Test config serialization."""
        config = OrchestratorConfig.default()
        data = config.to_dict()
        assert isinstance(data, dict)
        assert 'default_model' in data
        assert 'max_retries' in data


class TestWorklowState:
    """Tests for WorkflowState."""
    
    def test_state_initialization(self):
        """Test state initialization."""
        state = WorkflowState(
            workflow_id="test-123",
            topic="Test Topic",
            blogger_urls=["https://example.com"]
        )
        assert state.workflow_id == "test-123"
        assert state.topic == "Test Topic"
        assert len(state.blogger_urls) == 1
        assert len(state.errors) == 0
    
    def test_state_to_dict(self):
        """Test state serialization."""
        state = WorkflowState(
            workflow_id="test-123",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        data = state.to_dict()
        assert isinstance(data, dict)
        assert data['workflow_id'] == "test-123"
        assert data['topic'] == "Test"
    
    def test_state_to_json(self):
        """Test JSON serialization."""
        state = WorkflowState(
            workflow_id="test-123",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        json_str = state.to_json()
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data['workflow_id'] == "test-123"


class TestStateManager:
    """Tests for StateManager."""
    
    def test_start_phase(self):
        """Test starting a phase."""
        state = WorkflowState(
            workflow_id="test",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        manager = StateManager(state)
        
        manager.start_phase("test_phase", "TestAgent")
        assert "test_phase" in state.phases
        assert state.phases["test_phase"].status == PhaseStatus.RUNNING
        assert state.current_phase == "test_phase"
    
    def test_complete_phase(self):
        """Test completing a phase."""
        state = WorkflowState(
            workflow_id="test",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        manager = StateManager(state)
        
        manager.start_phase("test_phase")
        manager.complete_phase("test_phase", output="result")
        
        assert state.phases["test_phase"].status == PhaseStatus.COMPLETED
        assert state.phases["test_phase"].output == "result"
        assert state.phases["test_phase"].duration is not None
    
    def test_fail_phase(self):
        """Test failing a phase."""
        state = WorkflowState(
            workflow_id="test",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        manager = StateManager(state)
        
        manager.start_phase("test_phase")
        manager.fail_phase("test_phase", "Test error")
        
        assert state.phases["test_phase"].status == PhaseStatus.FAILED
        assert state.phases["test_phase"].error == "Test error"
        assert len(state.errors) == 1
    
    def test_skip_phase(self):
        """Test skipping a phase."""
        state = WorkflowState(
            workflow_id="test",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        manager = StateManager(state)
        
        manager.skip_phase("test_phase", "Not needed")
        
        assert state.phases["test_phase"].status == PhaseStatus.SKIPPED
        assert len(state.warnings) == 1
    
    def test_get_summary(self):
        """Test getting execution summary."""
        state = WorkflowState(
            workflow_id="test",
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        manager = StateManager(state)
        
        manager.start_phase("phase1")
        manager.complete_phase("phase1")
        manager.start_phase("phase2")
        manager.fail_phase("phase2", "error")
        
        summary = manager.get_summary()
        assert summary['phases_completed'] == 1
        assert summary['phases_failed'] == 1
        assert summary['total_phases'] == 2


class TestBloggerOrchestrator:
    """Tests for BloggerOrchestrator."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return OrchestratorConfig(
            openai_api_key="test-key",
            max_retries=1,
            verbose=False,
            enable_critique=False,
        )
    
    def test_orchestrator_initialization(self, config):
        """Test orchestrator initialization."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        assert orchestrator.config == config
        assert orchestrator.workflow is not None
    
    def test_orchestrator_run_basic(self, config):
        """Test basic orchestrator execution."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        
        result = orchestrator.run(
            topic="Test Topic",
            blogger_urls=["https://example.com"]
        )
        
        assert isinstance(result, dict)
        assert result['topic'] == "Test Topic"
        assert 'content' in result
        assert 'keywords' in result
        assert 'style_profile' in result
        assert 'image_prompts' in result
    
    def test_orchestrator_with_output_file(self, config, tmp_path):
        """Test orchestrator with output file."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        output_file = tmp_path / "test_output.json"
        
        result = orchestrator.run(
            topic="Test",
            blogger_urls=["https://example.com"],
            output_path=str(output_file)
        )
        
        assert output_file.exists()
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data['workflow_id'] == result['workflow_id']
    
    def test_orchestrator_get_state(self, config):
        """Test getting orchestrator state."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        
        # Before running
        assert orchestrator.get_state() is None
        
        # After running
        orchestrator.run(
            topic="Test",
            blogger_urls=["https://example.com"]
        )
        state = orchestrator.get_state()
        assert state is not None
        assert state.topic == "Test"

    def test_resolve_model_for_gemini_rewrites_incompatible_model(self):
        """Gemini provider must not keep HuggingFace model ids."""
        model = resolve_model_for_provider("gemini", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        assert model == "gemini-2.0-flash"

    def test_orchestrator_fails_on_empty_effective_content(self, config, monkeypatch):
        """Workflow must not report success if effective content is empty."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)

        monkeypatch.setattr(orchestrator.content_generator, "generate_draft", lambda **kwargs: "")
        monkeypatch.setattr(orchestrator.image_selector, "select_images", lambda **kwargs: [])

        with pytest.raises(RuntimeError, match="empty content"):
            orchestrator.run(topic="Test", blogger_urls=["https://example.com"])

    def test_gemini_provider_rejects_incompatible_model(self):
        """Gemini provider should reject explicit non-Gemini model ids."""
        if not GEMINI_AVAILABLE:
            pytest.skip("google-genai not installed")

        with pytest.raises(ValueError, match="incompatible with provider 'gemini'"):
            GeminiProvider(LLMConfig(api_key="dummy", model="meta-llama/Meta-Llama-3.1-8B-Instruct"))

    def test_pause_and_resume_continuous_publishing(self, config):
        """Continuous mode must expose pause/resume transitions."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        orchestrator.state_manager = StateManager(
            WorkflowState(workflow_id="w1", topic="continuous", blogger_urls=["https://example.com"])
        )

        paused = orchestrator.pause_continuous_publishing()
        assert paused["status"] == "paused"
        resumed = orchestrator.resume_continuous_publishing()
        assert resumed["status"] == "active"

    def test_continuous_publishing_single_cycle(self, config, monkeypatch):
        """Continuous bounded run should publish one successful cycle."""
        config.max_retries = 0
        orchestrator = BloggerOrchestrator(config=config, verbose=False)

        monkeypatch.setattr(orchestrator, "run", lambda **kwargs: {"workflow_id": "wf-1", "content": "ok"})
        result = orchestrator.start_continuous_publishing(
            blogger_urls=["https://example.com"],
            topic_candidates=[{"title": "AI", "category": "technology", "source": "test", "published_at": None}],
            cycles=1,
            interval_seconds=0,
        )

        assert result["summary"]["published"] == 1
        assert result["summary"]["failed"] == 0

    def test_continuous_publishing_skips_when_no_topic_candidate(self, config):
        """No valid topic should close cycle as skipped_with_reason."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        result = orchestrator.start_continuous_publishing(
            blogger_urls=["https://example.com"],
            topic_candidates=[],
            cycles=1,
            interval_seconds=0,
        )

        assert result["history"]["last_cycle"]["status"] == "source_exhausted"

    def test_continuous_publishing_marks_source_exhausted(self, config):
        """Untrusted-only sources should trigger source_exhausted."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        result = orchestrator.start_continuous_publishing(
            blogger_urls=["https://example.com"],
            topic_candidates=[{"title": "x", "category": "ai", "source": "https://evil.example"}],
            cycles=1,
            interval_seconds=0,
        )
        assert result["history"]["last_cycle"]["status"] == "source_exhausted"
        assert result["summary"]["failed"] == 1

    def test_retry_policy_backoff_sequence(self, config):
        """Retry schedule should keep 5m/15m/30m defaults."""
        config.max_retries = 3
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        assert list(orchestrator.retry_policy.iter_backoff_schedule()) == [300.0, 900.0, 1800.0]

    def test_operational_monitor_emits_alerts(self, config):
        """Monitor should alert when SLO thresholds are breached."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        orchestrator.history_store._state = {"cycles": [], "incidents": [], "published": []}
        now = datetime.now(timezone.utc)
        # Two failed cycles increase lag and reduce success rate.
        orchestrator.history_store.add_cycle(
            orchestrator._cycle_record(
                cycle_id="c1",
                topic="t1",
                status="failed",
                scheduled_at=(now - timedelta(hours=1)).isoformat(),
                started_at=(now - timedelta(hours=1)).isoformat(),
                ended_at=now.isoformat(),
                retry_count=3,
                reason="err",
                reason_code="provider_error",
                lag_minutes=120.0,
                trace={},
            )
        )
        orchestrator.history_store.add_cycle(
            orchestrator._cycle_record(
                cycle_id="c2",
                topic="t2",
                status="failed",
                scheduled_at=(now - timedelta(hours=2)).isoformat(),
                started_at=(now - timedelta(hours=2)).isoformat(),
                ended_at=now.isoformat(),
                retry_count=3,
                reason="err",
                reason_code="provider_error",
                lag_minutes=120.0,
                trace={},
            )
        )
        snapshot = orchestrator.monitor.evaluate()
        codes = {a["code"] for a in snapshot["alerts"]}
        assert "SLI_SUCCESS_RATE_BREACH" in codes
        assert "SLI_CYCLE_LAG_BREACH" in codes

    def test_get_operational_status_has_history(self, config):
        """Operational status endpoint should include history snapshot."""
        orchestrator = BloggerOrchestrator(config=config, verbose=False)
        status = orchestrator.get_operational_status()
        assert "operational" in status
        assert "history" in status


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

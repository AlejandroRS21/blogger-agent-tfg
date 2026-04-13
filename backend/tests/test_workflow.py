"""Tests for BloggerStyleWorkflow."""

import pytest
from datetime import datetime, timezone, timedelta
from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow
from aphra_blogger.context import BloggerContext
from src.orchestrator.continuous.scheduler import ContinuousScheduler
from src.orchestrator.state import WorkflowState, StateManager, OperationalStatus


def test_workflow_initialization():
    """Test that workflow initializes correctly."""
    workflow = BloggerStyleWorkflow()
    assert workflow.config is not None
    assert "models" in workflow.config
    assert workflow.context is None


def test_workflow_run_basic():
    """Test basic workflow execution."""
    workflow = BloggerStyleWorkflow()
    
    result = workflow.run(
        blogger_urls=["https://example.com/blog"],
        topic="Test Topic"
    )
    
    assert result is not None
    assert result["topic"] == "Test Topic"
    assert "keywords" in result
    assert "final_content" in result
    assert workflow.context is not None


def test_workflow_validation_empty_urls():
    """Test that workflow validates empty URLs."""
    workflow = BloggerStyleWorkflow()
    
    with pytest.raises(ValueError, match="At least one blogger URL is required"):
        workflow.run(blogger_urls=[], topic="Test Topic")


def test_workflow_validation_empty_topic():
    """Test that workflow validates empty topic."""
    workflow = BloggerStyleWorkflow()
    
    with pytest.raises(ValueError, match="Topic is required"):
        workflow.run(blogger_urls=["https://example.com"], topic="")


def test_context_creation():
    """Test BloggerContext creation."""
    context = BloggerContext(
        blogger_urls=["https://example.com"],
        topic="Test Topic"
    )
    
    assert context.blogger_urls == ["https://example.com"]
    assert context.topic == "Test Topic"
    assert context.draft_content == ""
    assert context.final_content == ""


def test_context_to_dict():
    """Test BloggerContext to_dict conversion."""
    context = BloggerContext(
        blogger_urls=["https://example.com"],
        topic="Test Topic"
    )
    
    data = context.to_dict()
    assert isinstance(data, dict)
    assert data["topic"] == "Test Topic"
    assert data["blogger_urls"] == ["https://example.com"]


def test_context_from_dict():
    """Test BloggerContext from_dict conversion."""
    data = {
        "blogger_urls": ["https://example.com"],
        "topic": "Test Topic",
        "style_profile": None,
        "keywords": [],
        "draft_content": "",
        "critique_feedback": None,
        "final_content": "",
        "html_structure": None,
        "image_prompts": [],
        "metadata": {}
    }
    
    context = BloggerContext.from_dict(data)
    assert context.topic == "Test Topic"
    assert context.blogger_urls == ["https://example.com"]


def test_continuous_scheduler_uses_12h_interval():
    """Continuous publishing must use a 12h default cadence."""
    scheduler = ContinuousScheduler(interval_hours=12)
    now = datetime.now(timezone.utc)
    next_run = scheduler.next_run_at(last_run_at=now)
    assert next_run - now == timedelta(hours=12)


def test_continuous_scheduler_lag_minutes():
    """Scheduler must expose cycle lag in minutes for monitoring."""
    scheduler = ContinuousScheduler(interval_hours=12)
    scheduled = datetime.now(timezone.utc) - timedelta(minutes=95)
    closed = datetime.now(timezone.utc)
    assert scheduler.cycle_lag_minutes(scheduled, closed) >= 95


def test_operational_snapshot_handles_degraded_status():
    """State manager should expose degraded status snapshots."""
    state = WorkflowState(workflow_id="w1", topic="t", blogger_urls=["https://example.com"])
    manager = StateManager(state)
    manager.set_operational_status(OperationalStatus.DEGRADED)
    snap = manager.get_operational_snapshot()
    assert snap["status"] == "degraded"

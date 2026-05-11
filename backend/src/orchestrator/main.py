"""
Main Orchestrator for Blogger Agent.

Coordinates all agents through a multi-phase workflow:
1. Style Analysis
2. Keyword Extraction
3. Content Generation
4. Critique & Refinement
5. HTML Building
6. Image Selection
"""

import time
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path

from .config import OrchestratorConfig
from .state import StateManager, WorkflowState, PhaseStatus, OperationalStatus
from .continuous import (
    AlertDispatcher,
    ContinuousScheduler,
    DraftValidator,
    HistoryStore,
    IncidentManager,
    OperationalMonitor,
    RetryPolicy,
    SourceGuard,
    TopicCandidate,
    TopicSelector,
)
from .safety import SafetyAgent
from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow
from aphra_blogger.context import BloggerContext
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.agents.keyword_extractor import KeywordExtractor
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.critic import CriticAgent
from aphra_blogger.agents.image_selector import ImageSelectorAgent
from aphra_blogger.agents.html_builder import HTMLBuilder


logger = logging.getLogger(__name__)


class BloggerOrchestrator:
    """
    Main orchestrator that coordinates all agents in the blogger workflow.
    
    This class implements a robust execution pipeline with:
    - Phase-based execution
    - Error handling and retries
    - Progress tracking
    - State persistence
    """
    
    def __init__(
        self,
        config: Optional[OrchestratorConfig] = None,
        verbose: bool = True
    ):
        """
        Initialize the orchestrator.
        
        Args:
            config: Configuration object. If None, uses default config.
            verbose: Whether to print progress messages.
        """
        if config is None:
            # Try to load from default location
            config_path = Path(__file__).parent.parent.parent / "aphra_blogger" / "config" / "default.toml"
            if config_path.exists():
                config = OrchestratorConfig.from_toml(str(config_path))
            else:
                config = OrchestratorConfig.default()
        
        config.validate()
        
        self.config = config
        self.verbose = verbose or config.verbose
        self.workflow = BloggerStyleWorkflow()
        self.state_manager = None
        self.history_store = HistoryStore()
        self.alert_dispatcher = AlertDispatcher(alerts=[])
        self.incident_manager = IncidentManager(self.history_store)
        self.monitor = OperationalMonitor(
            history_store=self.history_store,
            alert_dispatcher=self.alert_dispatcher,
            min_success_rate=0.95,
            max_lag_minutes=90.0,
        )
        self.scheduler = ContinuousScheduler(interval_hours=config.publish_interval_hours)
        self.retry_policy = RetryPolicy(
            max_retries=config.max_retries,
            backoff_seconds=config.continuous_backoff_seconds,
        )
        self.validator = DraftValidator(redundancy_threshold=config.redundancy_threshold)
        self.topic_selector = TopicSelector()
        self.source_guard = SourceGuard()
        
        # Initialize agents
        api_key = config.openai_api_key or config.huggingface_token or config.gemini_api_key or config.modal_api_key
        provider = config.provider
        
        # Determine shared API key for agents based on provider
        agent_api_key = api_key
        if provider == "gemini":
            agent_api_key = config.gemini_api_key
        elif provider == "openai":
            agent_api_key = config.openai_api_key
        elif provider == "huggingface":
            agent_api_key = config.huggingface_token
        elif provider == "modal":
            agent_api_key = config.modal_api_key
            
        self.safety_agent = SafetyAgent(api_key=agent_api_key, model=config.default_model, provider=provider)
        self.style_analyzer = StyleAnalyzer(api_key=agent_api_key, model=config.default_model, provider=provider)
        self.keyword_extractor = KeywordExtractor(api_key=agent_api_key, provider=provider)
        self.content_generator = ContentGenerator(api_key=agent_api_key, model=config.default_model, provider=provider)
        self.critic = CriticAgent(api_key=agent_api_key, model=config.default_model, provider=provider)
        self.image_selector = ImageSelectorAgent(api_key=agent_api_key, provider=provider)
        self.html_builder = HTMLBuilder()
    
    def _log(self, message: str, level: str = "INFO") -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            log_level = getattr(logging, level.upper(), logging.INFO)
            logger.log(log_level, message)

    def _classify_error(self, error_msg: str) -> str:
        """Classify error into a normalized error type."""
        message = (error_msg or "").lower()
        if "json" in message or "expecting value" in message:
            return "parse_error"
        if "timeout" in message:
            return "timeout"
        if "provider" in message or "api error" in message or "gemini" in message:
            return "provider_error"
        return "unknown"

    def _effective_model_for_agent(self, agent: Any) -> Optional[str]:
        """Best-effort extraction of effective model from an agent."""
        llm = getattr(agent, "llm", None)
        if not llm:
            return None
        if hasattr(llm, "model_id"):
            return getattr(llm, "model_id")
        llm_config = getattr(llm, "config", None)
        return getattr(llm_config, "model", None)
    
    def _execute_with_retry(
        self,
        phase_name: str,
        agent_name: str,
        func,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute a function with retry logic.
        
        Args:
            phase_name: Name of the current phase
            agent_name: Name of the agent
            func: Function to execute
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            Result of the function
            
        Raises:
            Exception: If all retries fail
        """
        retry_count = 0
        delay = self.config.retry_delay
        
        while retry_count <= self.config.max_retries:
            try:
                self._log(f"{phase_name}: Executing {agent_name}...")
                result = func(*args, **kwargs)
                
                if retry_count > 0:
                    self._log(f"{phase_name}: ✓ Succeeded after {retry_count} retries", "SUCCESS")
                else:
                    self._log(f"{phase_name}: ✓ Completed", "SUCCESS")
                
                return result
                
            except Exception as e:
                retry_count += 1
                error_msg = str(e)
                
                if retry_count <= self.config.max_retries:
                    self._log(
                        f"{phase_name}: ✗ Failed (attempt {retry_count}/{self.config.max_retries + 1}): {error_msg}",
                        "WARNING"
                    )
                    self.state_manager.fail_phase(
                        phase_name,
                        error_msg,
                        retry=True,
                        error_type=self._classify_error(error_msg),
                    )
                    time.sleep(delay)
                    delay *= self.config.backoff_factor
                else:
                    self._log(f"{phase_name}: ✗ Failed after {retry_count} attempts: {error_msg}", "ERROR")
                    raise
        
        raise RuntimeError(f"Unexpected error in retry logic for {phase_name}")
    
    def run(
        self,
        topic: str,
        blogger_urls: List[str],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete orchestrated workflow.
        
        Args:
            topic: Topic to write about
            blogger_urls: List of URLs to analyze for style
            output_path: Optional path to save workflow state JSON
            
        Returns:
            Dictionary with generated content and metadata
        """
        # Initialize state
        workflow_id = str(uuid.uuid4())[:8]
        state = WorkflowState(
            workflow_id=workflow_id,
            topic=topic,
            blogger_urls=blogger_urls,
        )
        self.state_manager = StateManager(state)
        
        self._log("=" * 60)
        self._log(f"Blogger Orchestrator Started [ID: {workflow_id}]")
        self._log(f"Topic: {topic}")
        self._log(f"Blogger URLs: {len(blogger_urls)} URL(s)")
        self._log("=" * 60)
        
        try:
            # Phase 0: Safety Validation
            phase = "safety_validation"
            self.state_manager.start_phase(phase, "SafetyAgent")
            safety_result = self.safety_agent.validate_topic(topic)
            
            if not safety_result.get("safe", False):
                reason = safety_result.get("reason", "Tema inapropiado")
                self.state_manager.fail_phase(phase, f"Seguridad: {reason}")
                raise ValueError(f"BLOQUEO DE SEGURIDAD: {reason}")
            
            self.state_manager.complete_phase(phase, output="Safe")
            self._log("Topic validated successfully.")

            # Phase 1: Style Analysis
            self._phase_style_analysis(blogger_urls)
            
            # Phase 2: Keyword Extraction
            self._phase_keyword_extraction(blogger_urls)
            
            # Phase 3: Content Generation (Draft)
            self._phase_content_generation_draft(topic)
            
            # Phase 4: Critique (if enabled)
            if self.config.enable_critique:
                self._phase_critique()
                
                # Phase 5: Refinement (if critique suggests changes)
                if self._needs_refinement():
                    self._phase_refinement()
                else:
                    state.final_content = state.draft_content
            else:
                self.state_manager.skip_phase("critique", "Critique disabled in config")
                self.state_manager.skip_phase("refinement", "Critique disabled")
                state.final_content = state.draft_content
            
            # Phase 6: HTML Building
            self._phase_html_building()
            
            # Phase 7: Image Selection
            self._phase_image_selection()

            # Guardrail: workflow cannot succeed with empty final output.
            effective_content = (state.final_content or state.draft_content or "").strip()
            if not effective_content:
                raise RuntimeError("Workflow produced empty content; refusing successful completion")
            
            # Finalize
            self.state_manager.mark_cycle_completed()
            self.state_manager.finalize()
            
            # Summary
            summary = self.state_manager.get_summary()
            self._log("=" * 60)
            self._log(f"Workflow Completed Successfully!")
            self._log(f"Duration: {summary['duration']:.2f}s")
            self._log(f"Phases: {summary['phases_completed']}/{summary['total_phases']} completed")
            if summary['warnings'] > 0:
                self._log(f"Warnings: {summary['warnings']}", "WARNING")
            self._log("=" * 60)
            
            # Save state if requested
            if output_path:
                self.state_manager.save_to_file(output_path)
                self._log(f"State saved to: {output_path}")
            
            # Return result
            result = self._build_result()

            if self.config.write_canonical_docs and self.state_manager.state.html_structure:
                published = self.html_builder.write_canonical_artifacts(
                    html_structure=self.state_manager.state.html_structure,
                    topic=topic,
                    docs_root=self.config.docs_output_dir,
                    content=result["content"],
                )
                result["metadata"]["published_record"] = published
                self.history_store.add_published(published)

            return result
            
        except Exception as e:
            self._log(f"Workflow Failed: {str(e)}", "ERROR")
            self.incident_manager.report(
                stage=self.state_manager.state.current_phase if self.state_manager else "workflow",
                reason_code=self._classify_error(str(e)),
                severity="major",
                recovery_action="retry",
            )
            if self.state_manager:
                self.state_manager.finalize()
                if output_path:
                    self.state_manager.save_to_file(output_path)
            raise

    def start_continuous_publishing(
        self,
        blogger_urls: List[str],
        topic_candidates: List[Dict[str, Any]],
        cycles: int = 1,
        interval_seconds: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Run bounded continuous publishing cycles (useful for cron or Modal jobs)."""
        if cycles <= 0:
            raise ValueError("cycles must be > 0")

        interval = interval_seconds if interval_seconds is not None else self.config.publish_interval_hours * 3600
        operational = {"published": 0, "failed": 0, "cycles": []}
        self.state_manager = StateManager(
            WorkflowState(
                workflow_id=str(uuid.uuid4())[:8],
                topic="continuous",
                blogger_urls=blogger_urls,
            )
        )
        self.state_manager.set_operational_status(OperationalStatus.ACTIVE)
        last_cycle_at = None

        for _ in range(cycles):
            if self.state_manager.state.pause_requested:
                break

            scheduled_at_dt = self.scheduler.next_run_at(last_run_at=last_cycle_at)
            cycle_id = str(uuid.uuid4())[:8]
            started_at_dt = datetime.now(timezone.utc)
            start_at = started_at_dt.isoformat()

            sanitized_candidates = self.source_guard.sanitize_candidates(topic_candidates)
            if not sanitized_candidates:
                self.history_store.add_cycle(
                    self._cycle_record(
                        cycle_id=cycle_id,
                        topic="source-exhausted",
                        status="source_exhausted",
                        scheduled_at=scheduled_at_dt.isoformat(),
                        started_at=start_at,
                        ended_at=datetime.now(timezone.utc).isoformat(),
                        retry_count=0,
                        reason="No trusted source candidates available",
                        reason_code="source_exhausted",
                        lag_minutes=self.scheduler.cycle_lag_minutes(scheduled_at_dt),
                        trace={"source_refs": [], "provider": self.config.provider},
                    )
                )
                self._emit_operational_event("source_exhausted", "major", cycle_id)
                operational["failed"] += 1
                self.state_manager.set_operational_status(OperationalStatus.DEGRADED)
                if interval > 0:
                    time.sleep(interval)
                continue

            selected = self.topic_selector.select(
                [
                    TopicCandidate(
                        title=item["title"],
                        category=item.get("category", "general"),
                        source=item.get("source", "unknown"),
                        published_at=item.get("published_at"),
                    )
                    for item in sanitized_candidates
                ]
            )
            if not selected:
                self.history_store.add_cycle(
                    self._cycle_record(
                        cycle_id=cycle_id,
                        topic="no-topic",
                        status="skipped_with_reason",
                        scheduled_at=scheduled_at_dt.isoformat(),
                        started_at=start_at,
                        ended_at=datetime.now(timezone.utc).isoformat(),
                        retry_count=0,
                        reason="No valid TopicCandidate after selection filters",
                        reason_code="no_topic_candidate",
                        lag_minutes=self.scheduler.cycle_lag_minutes(scheduled_at_dt),
                        trace={"source_refs": [c.get("source") for c in sanitized_candidates], "provider": self.config.provider},
                    )
                )
                self._emit_operational_event("skipped_with_reason", "warning", cycle_id)
                operational["cycles"].append(cycle_id)
                continue

            try:
                result = self.retry_policy.run(
                    lambda: self.run(topic=selected.title, blogger_urls=blogger_urls, output_path=None)
                )
                closed_at = datetime.now(timezone.utc)
                trace = {
                    "source_refs": [selected.source],
                    "provider": self.config.provider,
                    "topic_category": selected.category,
                    "prompt_fingerprint": f"{self.config.provider}:{self.config.default_model}:{selected.title}"[:120],
                }
                self.history_store.add_cycle(
                    self._cycle_record(
                        cycle_id=cycle_id,
                        topic=selected.title,
                        status="success",
                        scheduled_at=scheduled_at_dt.isoformat(),
                        started_at=start_at,
                        ended_at=closed_at.isoformat(),
                        retry_count=0,
                        reason_code="published",
                        lag_minutes=self.scheduler.cycle_lag_minutes(scheduled_at_dt, closed_at),
                        trace=trace,
                    )
                )
                generated_record = self.content_generator.build_generation_record(
                    topic=selected.title,
                    content=result.get("content", ""),
                    source_refs=[selected.source],
                    category=selected.category,
                )
                generated_record["published_at"] = closed_at.isoformat()
                generated_record["relevance_score"] = result.get("metadata", {}).get("relevance_score", 100.0)
                self.history_store.add_published(generated_record)
                operational["published"] += 1
                operational["cycles"].append(result.get("workflow_id"))
                self._emit_operational_event("cycle_success", "info", cycle_id)
                last_cycle_at = closed_at
            except Exception as exc:  # noqa: BLE001
                closed_at = datetime.now(timezone.utc)
                self.history_store.add_cycle(
                    self._cycle_record(
                        cycle_id=cycle_id,
                        topic=selected.title,
                        status="failed",
                        scheduled_at=scheduled_at_dt.isoformat(),
                        started_at=start_at,
                        ended_at=closed_at.isoformat(),
                        retry_count=self.config.max_retries,
                        reason=str(exc),
                        reason_code=self._classify_error(str(exc)),
                        lag_minutes=self.scheduler.cycle_lag_minutes(scheduled_at_dt, closed_at),
                        trace={"source_refs": [selected.source], "provider": self.config.provider, "topic_category": selected.category},
                    )
                )
                self.incident_manager.report(
                    stage="publish",
                    reason_code=self._classify_error(str(exc)),
                    severity="critical",
                    recovery_action="retry",
                )
                operational["failed"] += 1
                self._emit_operational_event("cycle_failed", "critical", cycle_id)

            if operational["failed"] > 0 and self._degradation_exceeds_threshold():
                self.state_manager.set_operational_status(OperationalStatus.DEGRADED)

            monitor_snapshot = self.monitor.evaluate()
            if self.history_store.should_pause_for_quality(min_relevance=70.0):
                self.state_manager.state.pause_requested = True
                self.state_manager.set_operational_status(OperationalStatus.PAUSED)
                self._emit_operational_event("quality_pause", "major", cycle_id)
            operational["monitoring"] = {
                "success_rate": monitor_snapshot["success_rate"],
                "avg_lag_minutes": monitor_snapshot["avg_lag_minutes"],
                "critical_open_incidents": monitor_snapshot["critical_open_incidents"],
            }

            if interval > 0:
                time.sleep(interval)

        return {
            "status": self.state_manager.get_operational_snapshot(),
            "summary": operational,
            "history": self.history_store.get_status_snapshot(),
            "alerts": self.alert_dispatcher.snapshot(),
        }

    def pause_continuous_publishing(self) -> Dict[str, Any]:
        """Pause continuous publishing while preserving scheduler state."""
        if not self.state_manager:
            raise RuntimeError("Continuous mode not initialized")
        self.state_manager.state.pause_requested = True
        self.state_manager.set_operational_status(OperationalStatus.PAUSED)
        return self.state_manager.get_operational_snapshot()

    def resume_continuous_publishing(self) -> Dict[str, Any]:
        """Resume continuous publishing after pause."""
        if not self.state_manager:
            raise RuntimeError("Continuous mode not initialized")
        self.state_manager.state.pause_requested = False
        self.state_manager.set_operational_status(OperationalStatus.ACTIVE)
        return self.state_manager.get_operational_snapshot()

    def get_operational_status(self) -> Dict[str, Any]:
        """Expose operational status and last cycles/incidents summary."""
        base = self.state_manager.get_operational_snapshot() if self.state_manager else {
            "status": OperationalStatus.PAUSED.value,
            "pause_requested": False,
            "last_cycle_at": None,
            "degradation_started_at": None,
            "errors": 0,
            "warnings": 0,
        }
        return {
            "operational": base,
            "history": self.history_store.get_status_snapshot(),
        }

    def _degradation_exceeds_threshold(self) -> bool:
        """Check if degraded runtime exceeded configured threshold."""
        if not self.state_manager:
            return False
        started = self.state_manager.state.degradation_started_at
        if started is None:
            self.state_manager.state.degradation_started_at = datetime.now(timezone.utc)
            return False
        elapsed = (datetime.now(timezone.utc) - started).total_seconds() / 3600.0
        return elapsed >= self.config.critical_degradation_hours

    def _cycle_record(
        self,
        cycle_id: str,
        topic: str,
        status: str,
        scheduled_at: str,
        started_at: str,
        ended_at: str,
        retry_count: int,
        reason: Optional[str] = None,
        reason_code: Optional[str] = None,
        lag_minutes: float = 0.0,
        trace: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Build cycle record object lazily to avoid import cycles."""
        from .continuous.history_store import CycleRecord

        return CycleRecord(
            cycle_id=cycle_id,
            scheduled_at=scheduled_at,
            started_at=started_at,
            ended_at=ended_at,
            status=status,
            topic=topic,
            retry_count=retry_count,
            reason=reason,
            reason_code=reason_code,
            lag_minutes=lag_minutes,
            trace=trace,
        )

    def _emit_operational_event(self, event: str, severity: str, cycle_id: str) -> None:
        """Emit an operational event to alert dispatcher and logger."""
        self.alert_dispatcher.emit(
            code=f"EVENT_{event.upper()}",
            message=f"Operational event: {event}",
            severity=severity,
            context={"cycle_id": cycle_id},
        )
    
    def _phase_style_analysis(self, blogger_urls: List[str]) -> None:
        """Phase 1: Analyze blogger style."""
        phase_name = "style_analysis"
        self.state_manager.start_phase(phase_name, "StyleAnalyzer")
        
        def analyze():
            return self.style_analyzer.analyze(blogger_urls)
        
        result = self._execute_with_retry(phase_name, "StyleAnalyzer", analyze)
        self.state_manager.state.style_profile = result
        self.state_manager.complete_phase(
            phase_name,
            result,
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.style_analyzer),
        )
    
    def _phase_keyword_extraction(self, blogger_urls: List[str]) -> None:
        """Phase 2: Extract keywords and phrases."""
        phase_name = "keyword_extraction"
        self.state_manager.start_phase(phase_name, "KeywordExtractor")
        
        def extract():
            extraction_result = self.keyword_extractor.extract(blogger_urls)
            # Return just the keywords list for backward compatibility
            return extraction_result.get("keywords", [])
        
        result = self._execute_with_retry(phase_name, "KeywordExtractor", extract)
        self.state_manager.state.keywords = result
        self.state_manager.complete_phase(
            phase_name,
            result,
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.keyword_extractor),
        )
    
    def _phase_content_generation_draft(self, topic: str) -> None:
        """Phase 3: Generate initial draft."""
        phase_name = "content_generation"
        self.state_manager.start_phase(phase_name, "ContentGenerator")
        
        def generate():
            style = self.state_manager.state.style_profile
            keywords = self.state_manager.state.keywords
            
            draft = self.content_generator.generate_draft(
                topic=topic,
                style_profile=style,
                keywords=keywords,
                min_words=self.config.min_word_count,
                max_words=self.config.max_word_count
            )
            return draft
        
        result = self._execute_with_retry(phase_name, "ContentGenerator", generate)
        self.state_manager.state.draft_content = result
        fallback_used = result.strip().startswith("# ") and "A ver, que me habéis preguntado mucho" in result
        self.state_manager.complete_phase(
            phase_name,
            output=f"{len(result)} characters",
            fallback_used=fallback_used,
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.content_generator),
        )
    
    def _phase_critique(self) -> None:
        """Phase 4: Critique the draft."""
        phase_name = "critique"
        self.state_manager.start_phase(phase_name, "CriticAgent")
        
        def critique():
            draft = self.state_manager.state.draft_content
            style = self.state_manager.state.style_profile
            topic = self.state_manager.state.topic
            
            return self.critic.critique(
                content=draft,
                style_profile=style,
                topic=topic
            )
        
        result = self._execute_with_retry(phase_name, "CriticAgent", critique)
        self.state_manager.state.critique_feedback = str(result)
        self.state_manager.state.metadata['critique_result'] = result
        self.state_manager.complete_phase(
            phase_name,
            result,
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.critic),
        )
    
    def _needs_refinement(self) -> bool:
        """Check if content needs refinement based on critique."""
        if not self.state_manager.state.metadata.get('critique_result'):
            return False
        
        critique_result = self.state_manager.state.metadata['critique_result']
        
        # Check if critique suggests revision
        if isinstance(critique_result, dict):
            return critique_result.get('needs_revision', False)
        
        return False
    
    def _phase_refinement(self) -> None:
        """Phase 5: Refine content based on critique."""
        phase_name = "refinement"
        self.state_manager.start_phase(phase_name, "ContentGenerator")
        
        def refine():
            draft = self.state_manager.state.draft_content
            critique = self.state_manager.state.metadata.get('critique_result', {})
            style = self.state_manager.state.style_profile
            
            refined = self.content_generator.refine_content(
                draft=draft,
                critique_feedback=critique,
                style_profile=style,
            )
            return refined
        
        result = self._execute_with_retry(phase_name, "ContentGenerator", refine)
        self.state_manager.state.final_content = result
        self.state_manager.complete_phase(
            phase_name,
            output=f"{len(result)} characters",
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.content_generator),
        )
    def _phase_html_building(self) -> None:
        """Phase 6: Build HTML structure."""
        phase_name = "html_building"
        self.state_manager.start_phase(phase_name, "HTMLBuilder")
        
        def build():
            # Use final content if available, otherwise use draft
            content = self.state_manager.state.final_content or self.state_manager.state.draft_content
            topic = self.state_manager.state.topic
            style_profile = self.state_manager.state.style_profile
            
            # Note: images will be selected in the next phase
            # For now, build HTML/JSX without images
            html_output = self.html_builder.build(
                content=content,
                topic=topic,
                images=None,  # Images come from next phase
                style_profile=style_profile
            )
            
            # Generate slug from topic (lowercase, replace spaces with hyphens)
            slug = topic.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Convert to dictionary for state storage
            return {
                "html": html_output.html,
                "jsx": html_output.jsx,
                "metadata": {
                    "title": html_output.meta_title,
                    "description": html_output.meta_description,
                    "keywords": html_output.meta_keywords,
                    "reading_time": html_output.reading_time,
                    "word_count": html_output.word_count,
                    "slug": slug,
                },
                "headings": html_output.headings,
                "nextjs_component": self.html_builder.generate_nextjs_component(html_output, slug)
            }
        
        result = self._execute_with_retry(phase_name, "HTMLBuilder", build)
        self.state_manager.state.html_structure = result
        self.state_manager.complete_phase(
            phase_name,
            result['metadata'],
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.html_builder),
        )
    
    def _phase_image_selection(self) -> None:
        """Phase 7: Select and place images."""
        phase_name = "image_selection"
        self.state_manager.start_phase(phase_name, "ImageSelectorAgent")
        
        def select():
            content = self.state_manager.state.final_content or self.state_manager.state.draft_content
            topic = self.state_manager.state.topic
            
            return self.image_selector.select_images(
                content=content,
                topic=topic,
                num_images=3
            )
        
        result = self._execute_with_retry(phase_name, "ImageSelectorAgent", select)
        self.state_manager.state.image_prompts = result
        fallback_used = bool(result and isinstance(result, list) and "Professional, modern hero image" in result[0].get("prompt", ""))
        self.state_manager.complete_phase(
            phase_name,
            result,
            fallback_used=fallback_used,
            effective_provider=self.config.provider,
            effective_model=self._effective_model_for_agent(self.image_selector),
        )
    
    def _build_result(self) -> Dict[str, Any]:
        """Build final result dictionary."""
        state = self.state_manager.state
        
        return {
            "workflow_id": state.workflow_id,
            "topic": state.topic,
            "blogger_urls": state.blogger_urls,
            "style_profile": state.style_profile,
            "keywords": state.keywords,
            "content": state.final_content or state.draft_content,
            "html_structure": state.html_structure,
            "image_prompts": state.image_prompts,
            "metadata": {
                "duration": state.total_duration,
                "phases": {
                    name: phase.to_dict()
                    for name, phase in state.phases.items()
                },
                "errors": state.errors,
                "warnings": state.warnings,
            }
        }
    
    def get_state(self) -> Optional[WorkflowState]:
        """Get current workflow state."""
        return self.state_manager.state if self.state_manager else None

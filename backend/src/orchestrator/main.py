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
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from .config import OrchestratorConfig
from .state import StateManager, WorkflowState, PhaseStatus
from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow
from aphra_blogger.context import BloggerContext
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.agents.keyword_extractor import KeywordExtractor
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.critic import CriticAgent
from aphra_blogger.agents.image_selector import ImageSelectorAgent
from aphra_blogger.agents.html_builder import HTMLBuilder


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
        self.state_manager: Optional[StateManager] = None
        
        # Initialize agents
        api_key = config.openai_api_key
        self.style_analyzer = StyleAnalyzer(api_key=api_key, model=config.default_model)
        self.keyword_extractor = KeywordExtractor(api_key=api_key)
        self.content_generator = ContentGenerator(api_key=api_key, model=config.default_model)
        self.critic = CriticAgent(api_key=api_key, model=config.default_model)
        self.image_selector = ImageSelectorAgent(api_key=api_key)
        self.html_builder = HTMLBuilder()
    
    def _log(self, message: str, level: str = "INFO") -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
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
                    self.state_manager.fail_phase(phase_name, error_msg, retry=True)
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
                self.state_manager.skip_phase("critique", "Critique disabled in config")
                self.state_manager.skip_phase("refinement", "Critique disabled")
                state.final_content = state.draft_content
            
            # Phase 6: HTML Building
            self._phase_html_building()
            
            # Phase 7: Image Selection
            self._phase_image_selection()
            
            # Finalize
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
            return self._build_result()
            
        except Exception as e:
            self._log(f"Workflow Failed: {str(e)}", "ERROR")
            if self.state_manager:
                self.state_manager.finalize()
                if output_path:
                    self.state_manager.save_to_file(output_path)
            raise
    
    def _phase_style_analysis(self, blogger_urls: List[str]) -> None:
        """Phase 1: Analyze blogger style."""
        phase_name = "style_analysis"
        self.state_manager.start_phase(phase_name, "StyleAnalyzer")
        
        def analyze():
            return self.style_analyzer.analyze(blogger_urls)
        
        result = self._execute_with_retry(phase_name, "StyleAnalyzer", analyze)
        self.state_manager.state.style_profile = result
        self.state_manager.complete_phase(phase_name, result)
    
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
        self.state_manager.complete_phase(phase_name, result)
    
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
        self.state_manager.complete_phase(phase_name, output=f"{len(result)} characters")
    
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
        self.state_manager.complete_phase(phase_name, result)
    
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
            keywords = self.state_manager.state.keywords
            
            refined = self.content_generator.refine_content(
                draft=draft,
                critique_feedback=critique,
                style_profile=style,
                keywords=keywords
            )
            return refined
        
        result = self._execute_with_retry(phase_name, "ContentGenerator", refine)
        self.state_manager.state.final_content = result
        self.state_manager.complete_phase(phase_name, output=f"{len(result)} characters")
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
        self.state_manager.complete_phase(phase_name, result['metadata'])
    
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
        self.state_manager.complete_phase(phase_name, result)
    
    def _build_result(self) -> Dict[str, Any]:
        """Build final result dictionary."""
        state = self.state_manager.state
        
        return {
            "workflow_id": state.workflow_id,
            "topic": state.topic,
            "blogger_urls": state.blogger_urls,
            "style_profile": state.style_profile,
            "keywords": state.keywords,
            "content": state.final_content,
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

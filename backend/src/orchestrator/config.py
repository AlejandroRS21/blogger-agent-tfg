"""
Orchestrator configuration module.

Manages configuration for the blogger orchestrator including
LLM settings, retry policies, and workflow parameters.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import toml
from pathlib import Path


@dataclass
class OrchestratorConfig:
    """Configuration for the BloggerOrchestrator."""
    
    # LLM Settings
    default_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Retry Settings
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds
    backoff_factor: float = 2.0
    
    # Workflow Settings
    enable_critique: bool = True
    max_critique_iterations: int = 2
    verbose: bool = True
    
    # Content Settings
    min_word_count: int = 800
    max_word_count: int = 2500
    
    # API Keys (from environment)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Timeouts
    agent_timeout: int = 60  # seconds per agent
    
    # Additional settings
    extra: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_toml(cls, config_path: str) -> "OrchestratorConfig":
        """Load configuration from TOML file."""
        with open(config_path, 'r') as f:
            data = toml.load(f)
        
        # Extract relevant sections
        models = data.get('models', {})
        workflow = data.get('workflow', {})
        content = data.get('content', {})
        
        return cls(
            default_model=models.get('default_model', 'gpt-4-turbo-preview'),
            temperature=models.get('openai', {}).get('temperature', 0.7),
            max_tokens=models.get('openai', {}).get('max_tokens', 2000),
            enable_critique=workflow.get('enable_critic', True),
            max_critique_iterations=workflow.get('max_iterations', 2),
            verbose=workflow.get('verbose', True),
            min_word_count=content.get('min_word_count', 800),
            max_word_count=content.get('max_word_count', 2500),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        )
    
    @classmethod
    def default(cls) -> "OrchestratorConfig":
        """Create default configuration."""
        return cls(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        )
    
    def validate(self) -> None:
        """Validate configuration."""
        if not self.openai_api_key and not self.anthropic_api_key:
            raise ValueError(
                "At least one API key must be set: OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        
        if self.min_word_count > self.max_word_count:
            raise ValueError("min_word_count cannot be greater than max_word_count")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'default_model': self.default_model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'max_retries': self.max_retries,
            'enable_critique': self.enable_critique,
            'verbose': self.verbose,
        }

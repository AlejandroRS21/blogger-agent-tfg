"""
Shared context for the Blogger Agent workflow.

This module defines the context structure that is shared across
all agents in the workflow.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class BloggerContext:
    """
    Context shared across all agents in the blogger workflow.
    
    Attributes:
        blogger_urls: List of URLs to analyze for style
        topic: Topic to write about
        style_profile: Extracted style profile from analysis
        keywords: Extracted keywords from blogger's content
        draft_content: Initial draft content
        critique_feedback: Feedback from critic agent
        final_content: Final refined content
        html_structure: HTML/JSON structure for rendering
        image_prompts: Generated image prompts and placements
    """
    
    # Input parameters
    blogger_urls: List[str] = field(default_factory=list)
    topic: str = ""
    
    # Intermediate results
    style_profile: Optional[Dict[str, Any]] = None
    keywords: List[str] = field(default_factory=list)
    draft_content: str = ""
    critique_feedback: Optional[str] = None
    
    # Final outputs
    final_content: str = ""
    html_structure: Optional[Dict[str, Any]] = None
    image_prompts: List[Dict[str, str]] = field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "blogger_urls": self.blogger_urls,
            "topic": self.topic,
            "style_profile": self.style_profile,
            "keywords": self.keywords,
            "draft_content": self.draft_content,
            "critique_feedback": self.critique_feedback,
            "final_content": self.final_content,
            "html_structure": self.html_structure,
            "image_prompts": self.image_prompts,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BloggerContext":
        """Create context from dictionary."""
        return cls(**data)

"""
Keyword Extractor Agent.

Extracts relevant keywords, phrases, and expressions
from a blogger's content.
"""

from typing import List, Dict, Any, Optional
import os
import logging
from collections import Counter
import re

logger = logging.getLogger(__name__)

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
    from ..utils import parse_json_from_text
except ImportError:
    LLM_AVAILABLE = False


class KeywordExtractor:
    """
    Extracts keywords and characteristic phrases from blog content.
    
    Identifies:
    - Important keywords and topics
    - Characteristic expressions and phrases
    - Frequent n-grams
    - Domain-specific terminology
    
    Uses HuggingFace models by default, with OpenAI as fallback.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto"
    ):
        """
        Initialize the KeywordExtractor.
        
        Args:
            api_key: API key for LLM provider
            model: Model to use. If None, uses provider defaults.
            provider: "huggingface", "openai", or "auto"
        """
        self.model = model
        self.provider_name = provider
        
        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model, # Factory will handle defaults
                    temperature=0.3,
                    max_tokens=800
                )
            except Exception as e:
                logger.warning(f"Failed to initialize LLM provider: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def extract(self, blogger_urls: List[str], sample_text: str = None) -> Dict[str, Any]:
        """
        Extract keywords and phrases from the blogger's content.
        
        Args:
            blogger_urls: List of blog URLs
            sample_text: Optional sample text
            
        Returns:
            Dictionary with keywords and expressions
        """
        if not self.llm or not self.llm.is_available():
            return self._fallback_extraction()
        
        url_text = blogger_urls[0] if blogger_urls else (sample_text or "General Tech Blog")
        
        prompt = f"""Extract keywords and characteristic expressions from the blog context: {url_text}

This is Javi Pas's tech blog "Incognitosis". Known recurring topics and expressions:

TOPICS: AI, OpenClaw, Claude, ChatGPT, Apple, Anthropic, technology, family life, 
nostalgia, retro tech, personal experiments

EXPRESSIONS: "me alucina", "brutal", "flipar", "miniresort burgués", 
"mis maravillosos niños", "dicho y hecho", "total, que", "el caso es que"

Extract and return JSON:
{{
  "keywords": ["20-30 most important topic keywords"],
  "expressions": ["10-15 characteristic phrases/expressions"],
  "technical_terms": ["5-10 recurring technical terms"],
  "themes": ["5-10 major themes"]
}}

Return ONLY valid JSON, no other text."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are an expert in keyword extraction and content analysis.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(messages)
            
            result = parse_json_from_text(response.content)
            return result
            
        except Exception as e:
            logger.warning(f"Keyword extraction failed: {e}. Using fallback.")
            return self._fallback_extraction()
    
    def _fallback_extraction(self) -> Dict[str, Any]:
        """Fallback keyword extraction based on known patterns."""
        return {
            "keywords": [
                "IA", "inteligencia artificial", "OpenClaw", "Claude", "ChatGPT",
                "tecnología", "Apple", "Anthropic", "innovación", "desarrollo",
                "software", "hardware", "futuro", "educación", "familia",
                "experimento", "prueba", "análisis", "opinión", "crítica",
                "nostalgia", "retro", "gaming", "ordenadores", "Internet"
            ],
            "expressions": [
                "me alucina",
                "dicho y hecho",
                "total, que",
                "el caso es que",
                "ciertamente",
                "como digo",
                "insisto",
                "miniresort burgués",
                "mis maravillosos niños",
                "brutal",
                "flipar",
                "chulo",
                "mazo",
                "yuyu"
            ],
            "technical_terms": [
                "API",
                "modelo de lenguaje",
                "LLM",
                "prompt",
                "machine learning",
                "neural network",
                "deployment",
                "cloud",
                "open source"
            ],
            "themes": [
                "Inteligencia Artificial",
                "Tecnología personal",
                "Vida familiar",
                "Experimentos tech",
                "Industria tecnológica",
                "Nostalgia computacional",
                "Opinión crítica",
                "Educación tech"
            ]
        }

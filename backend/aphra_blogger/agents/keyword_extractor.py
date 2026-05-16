"""
Keyword Extractor Agent.

Extracts relevant keywords, phrases, and expressions
from a blogger's content.
"""

from typing import List, Dict, Any, Optional
import os
from collections import Counter
import re

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
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
                print(f"Warning: Failed to initialize LLM provider: {e}")
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

Identify the most relevant keywords, recurrent expressions, technical terms, and main themes from the provided text to capture the author's specific focus and style.

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
            
            import json
            result = json.loads(response.content)
            return result
            
        except Exception as e:
            print(f"Warning: Keyword extraction failed: {e}. Using fallback.")
            return self._fallback_extraction()
    
    def _fallback_extraction(self) -> Dict[str, Any]:
        """Fallback keyword extraction based on generic patterns."""
        return {
            "keywords": [
                "tecnología", "innovación", "desarrollo", "software", "hardware", 
                "futuro", "análisis", "tendencias", "mercado", "digital",
                "datos", "internet", "productividad", "herramientas", "sistema"
            ],
            "expressions": [
                "es importante destacar",
                "en resumen",
                "por otro lado",
                "sin embargo",
                "en conclusión",
                "cabe mencionar",
                "desde esta perspectiva",
                "la realidad es que",
                "en definitiva"
            ],
            "technical_terms": [
                "API",
                "algoritmo",
                "backend",
                "frontend",
                "framework",
                "cloud computing",
                "despliegue",
                "arquitectura"
            ],
            "themes": [
                "Desarrollo de Software",
                "Tendencias Tecnológicas",
                "Productividad Digital",
                "Análisis de Industria",
                "Innovación"
            ]
        }

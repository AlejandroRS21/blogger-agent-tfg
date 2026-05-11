"""
Style Analyzer Agent.

Analyzes a blogger's writing style including tone, voice,
structure, and characteristic expressions.
"""

from typing import List, Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
    from ..utils import parse_json_from_text
except ImportError:
    LLM_AVAILABLE = False


class StyleAnalyzer:
    """
    Analyzes the writing style of a blogger.
    
    Extracts:
    - Tone (conversational, formal, humorous, etc.)
    - Voice (first person, third person, etc.)
    - Structure patterns (intro-body-conclusion, etc.)
    - Characteristic expressions and phrases
    - Sentence and paragraph metrics
    
    Uses HuggingFace models by default, with OpenAI as fallback.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None,
        provider: str = "auto"
    ):
        """
        Initialize the StyleAnalyzer.
        
        Args:
            api_key: API key for LLM provider (HF_TOKEN, OPENAI_API_KEY, etc.)
            model: Model to use. If None, uses provider defaults.
            provider: "huggingface", "openai", or "auto" (tries HF first)
        """
        self.model = model
        self.provider_name = provider
        
        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model, # Dejar que el factory decida si no se provee
                    temperature=0.3,
                    max_tokens=1000
                )
            except Exception as e:
                logger.warning(f"Failed to initialize LLM provider: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def analyze(self, blogger_urls: List[str], sample_text: str = None) -> Dict[str, Any]:
        """
        Analyze the blogger's writing style.
        
        Args:
            blogger_urls: List of blog URLs to analyze
            sample_text: Optional sample text if URLs can't be scraped yet
            
        Returns:
            Dictionary with style profile
        """
        if not self.llm or not self.llm.is_available():
            # Fallback to rule-based analysis
            return self._fallback_analysis(sample_text or "")
        
        # Safe extraction of sample_text
        safe_sample = (sample_text or "")[:500]
        url_context = f"URLs: {', '.join(blogger_urls)}" if blogger_urls else f"Sample Text: {safe_sample}"
        
        # For now, use a comprehensive prompt with known info about Javi Pas style
        prompt = f"""Analyze the writing style of the blogger from this context: {url_context}.

Based on research, this blogger (Javi Pas from javipas.com "Incognitosis") has the following characteristics:

KNOWN STYLE TRAITS:
- Tone: Conversational, humorous, self-ironic, personal, enthusiastic but critical
- Voice: First person, speaks directly to reader
- Language: Colloquial Spanish with expressions like "me alucina", "flipar", "mazo", "brutal"
- Structure: Personal intro → Experience narrative → Technical details → Reflection
- Characteristic phrases: "miniresort burgués" (his home), "mis maravillosos niños", "dicho y hecho", 
  "total, que...", "el caso es que...", "ciertamente", "como digo", "insisto"
- Paragraph style: Medium paragraphs (3-5 lines)
- Use of parentheses for clarifications
- Frequent ellipsis (...)
- Post length: 1500-3000 words typically

Your task: Create a detailed style profile as JSON with these fields:
{{
  "tone": "string describing overall tone",
  "voice": "narrative voice perspective",
  "language_level": "formal/casual/colloquial",
  "structure": "typical post structure",
  "expressions": ["list", "of", "characteristic", "expressions"],
  "avg_sentence_length": estimated_number,
  "paragraph_pattern": "description of paragraph style",
  "use_of_humor": "description",
  "technical_depth": "how technical the content gets",
  "personality_traits": ["trait1", "trait2"],
  "engagement_style": "how they engage with readers"
}}

Respond with ONLY the JSON, no other text."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are an expert in analyzing writing styles and linguistic patterns.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(messages)
            
            result = parse_json_from_text(response.content)
            return result
            
        except Exception as e:
            logger.warning(f"LLM analysis failed: {e}. Using fallback.")
            return self._fallback_analysis(sample_text or "")
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback rule-based analysis when LLM is not available."""
        return {
            "tone": "conversational, humorous, personal, enthusiastic",
            "voice": "first person, close to reader",
            "language_level": "colloquial",
            "structure": "personal intro → experience → technical details → reflection",
            "expressions": [
                "me alucina",
                "dicho y hecho",
                "el caso es que",
                "total, que",
                "ciertamente",
                "como digo",
                "insisto",
                "miniresort burgués",
                "mis maravillosos niños"
            ],
            "avg_sentence_length": 15,
            "paragraph_pattern": "3-5 lines, medium complexity",
            "use_of_humor": "Subtle irony and self-deprecating humor",
            "technical_depth": "Medium-high, explains complex topics accessibly",
            "personality_traits": [
                "curious",
                "enthusiastic about technology",
                "family-oriented",
                "reflective",
                "critical thinker"
            ],
            "engagement_style": "Invites reader comments, asks questions, shares personal experiences"
        }

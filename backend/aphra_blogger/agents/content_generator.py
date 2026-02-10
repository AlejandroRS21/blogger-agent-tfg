"""
Content Generator Agent.

Generates blog content in the style of the analyzed blogger.
"""

from typing import Dict, Any, Optional
import os

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


class ContentGenerator:
    """
    Generates blog content based on a topic and style profile.
    
    Creates:
    - Initial draft content
    - Styled content matching blogger's voice
    - Refined content based on critique
    
    Uses HuggingFace models by default (Llama 3.1 70B for best quality).
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto"
    ):
        """
        Initialize the ContentGenerator.
        
        Args:
            api_key: API key for LLM provider
            model: Model to use. If None, uses high-quality model for generation.
            provider: "huggingface", "openai", or "auto"
        """
        self.model = model
        self.provider_name = provider
        
        if LLM_AVAILABLE:
            try:
                # Use best model for content generation
                default_model = model or "meta-llama/Meta-Llama-3.1-70B-Instruct"
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=default_model,
                    temperature=0.8,
                    max_tokens=3000
                )
            except Exception as e:
                print(f"Warning: Failed to initialize LLM provider: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def generate_draft(
        self,
        topic: str,
        style_profile: Dict[str, Any],
        keywords: list,
        min_words: int = 1500,
        max_words: int = 2500
    ) -> str:
        """
        Generate initial draft content.
        
        Args:
            topic: Topic to write about
            style_profile: Style profile from StyleAnalyzer
            keywords: Keywords from KeywordExtractor
            min_words: Minimum word count
            max_words: Maximum word count
            
        Returns:
            Draft content as markdown string
        """
        if not self.llm or not self.llm.is_available():
            return self._fallback_draft(topic, keywords)
        
        # Build comprehensive prompt
        expressions_str = ", ".join(style_profile.get("expressions", [])[:8])
        keywords_str = ", ".join(keywords[:15])
        
        prompt = f"""Write a blog post about: {topic}

STYLE REQUIREMENTS:
- Tone: {style_profile.get('tone', 'conversational and personal')}
- Voice: {style_profile.get('voice', 'first person')}
- Structure: {style_profile.get('structure', 'intro-body-conclusion')}
- Language: Use expressions like: {expressions_str}
- Related keywords: {keywords_str}

CONTENT GUIDELINES:
- Length: {min_words}-{max_words} words
- Start with a personal intro (like "Sé que estoy un poco pesado con el tema, pero...")
- Include personal anecdotes or experiences
- Mix technical details with accessible explanations
- Use short-medium paragraphs (3-5 lines)
- Add occasional parentheses for clarifications
- End inviting reader engagement
- Use markdown format for structure (# for title, ## for sections)

BLOGGER PERSONALITY (Javi Pas style):
- Enthusiastic about technology but critically analytical
- References family life ("miniresort burgués", "mis maravillosos niños")
- Self-ironic and humble
- Uses colloquial Spanish expressions naturally
- Shares personal experiments and tests

Write a complete, engaging blog post. Use only markdown, no code blocks."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are Javi Pas, a Spanish tech blogger known for your conversational, humorous, and personal writing style about technology, AI, and personal experiments.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(
                messages,
                temperature=0.8,
                max_tokens=3000
            )
            
            return response.content
            
        except Exception as e:
            print(f"Warning: Content generation failed: {e}. Using fallback.")
            return self._fallback_draft(topic, keywords)
    
    def refine_content(
        self,
        draft: str,
        critique_feedback: Dict[str, Any],
        style_profile: Dict[str, Any]
    ) -> str:
        """
        Refine content based on critique feedback.
        
        Args:
            draft: Original draft
            critique_feedback: Feedback from CriticAgent
            style_profile: Style profile for reference
            
        Returns:
            Refined content
        """
        if not self.llm or not self.llm.is_available():
            return draft  # Return original if no LLM available
        
        suggestions = critique_feedback.get('suggestions', [])
        suggestions_str = "\\n".join(f"- {s}" for s in suggestions)
        
        prompt = f"""Refine this blog post based on the critique feedback.

ORIGINAL CONTENT:
{draft}

CRITIQUE FEEDBACK:
Coherence Score: {critique_feedback.get('coherence_score', 'N/A')}/10
Style Match: {critique_feedback.get('style_match', 'N/A')}/10

SUGGESTIONS:
{suggestions_str}

INSTRUCTIONS:
- Keep the same overall structure and tone
- Address the suggestions while maintaining the blogger's voice
- Ensure smooth transitions and coherence
- Preserve personal anecdotes and expressions
- Keep the length similar (don't add too much)

Provide the refined version in markdown format."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are an editor helping improve blog posts while maintaining the author's unique voice.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(
                messages,
                temperature=0.7,
                max_tokens=3500
            )
            
            return response.content
            
        except Exception as e:
            print(f"Warning: Refinement failed: {e}. Returning original draft.")
            return draft
    
    def _fallback_draft(self, topic: str, keywords: list) -> str:
        """Generate a basic draft when LLM is not available."""
        keywords_str = ", ".join(keywords[:5]) if keywords else "tecnología, innovación"
        
        return f"""# {topic}

Sé que estoy un poco pesado con el tema, pero {topic} me tiene fascinado últimamente.

## Contexto

El caso es que hace unos días decidí investigar más sobre esto. Total, que me puse manos a la obra y lo que descubrí me dejó bastante sorprendido. Llevo años siguiendo este tipo de cosas, pero cada vez que profundizo encuentro algo nuevo que me alucina.

## Lo que he aprendido

Primero, hay que entender el contexto. {topic} no es algo que haya surgido de la noche a la mañana. Lleva años desarrollándose, pero ahora es cuando realmente empieza a tener sentido. La conexión con {keywords_str} es fundamental para entender su importancia.

Dicho y hecho, me lancé a probarlo por mi cuenta. Y ciertamente, los resultados son bastante chulos. No es perfecto, obviamente, pero tiene un potencial brutal.

## Mi experiencia personal

En mi miniresort burgués, mis maravillosos niños me preguntaron sobre esto. Y ahí me di cuenta de lo importante que es explicar estas cosas de manera sencilla. La tecnología avanza a un ritmo brutal, y {topic} es un ejemplo perfecto de ello.

He estado experimentando con diferentes enfoques, y cada uno tiene su punto. Algunos funcionan mejor que otros, pero todos aportan algo interesante al conjunto.

## Reflexión final

Insisto: vale la pena prestarle atención a {topic}. No es solo hype, hay sustancia detrás. Como digo siempre, el tiempo lo dirá. Pero por ahora, yo estoy bastante optimista.

La clave está en entender no solo cómo funciona, sino por qué es importante. Y eso es algo que solo se consigue probando, equivocándose, y aprendiendo del proceso.

## Conclusión

Total, que aquí estamos. {topic} sigue evolucionando, y yo seguiré experimentando con ello. Si tenéis comentarios y sugerencias, invitados estáis a compartirlos.

Como siempre, esto es solo el principio. Lo interesante está por llegar.
"""

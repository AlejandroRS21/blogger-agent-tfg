"""
Content Generator Agent.

Generates blog content in the style of the analyzed blogger.
Supports dynamic structural diversity and varied opening hooks.
"""

from typing import Dict, Any, Optional, List
import random
import logging

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


logger = logging.getLogger(__name__)


class ContentGenerator:
    """
    Generates blog content based on a topic and style profile.
    
    Supports "Anti-template" generation by injecting varied structural intents.
    """
    
    STRUCTURAL_MODES = {
        "REFLECTIVE": "Ensayo largo y reflexivo. Párrafos medios-largos. Menos subtítulos, más flujo narrativo.",
        "TECHNICAL": "Análisis técnico de cacharreo. Listas de especificaciones, comparativas y muchas negritas.",
        "QUICK_FLASH": "Post corto y directo. Una idea potente, una pregunta al lector y poca paja.",
        "CURATED_LINKS": "Curación de contenidos. Un enlace principal con un comentario mordaz y contexto.",
        "RANT": "Opinión crítica y apasionada. Oraciones cortas, muchas exclamaciones y tono muy personal."
    }

    OPENING_HOOKS = [
        "CONFESSION: Admitir una obsesión con el tema o una 'cruzada particular'.",
        "REACTION: Reacción instantánea de incredulidad o sorpresa ante una noticia.",
        "HISTORICAL: Referencia nostálgica a tecnologías antiguas (procesadores 486, Spectrum).",
        "FAMILIAR: Enmarcar el tema en una situación cotidiana en el 'miniresort burgués' con familia.",
        "RHETORICAL: Lanzar una pregunta desafiante que rompa la cuarta pared."
    ]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto"
    ):
        self.model = model
        self.provider_name = provider
        
        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model,
                    temperature=0.85, # Increased for more structural variety
                    max_tokens=3500
                )
            except Exception as e:
                logger.warning("Failed to initialize LLM provider: %s", e)
                self.llm = None
        else:
            self.llm = None

    def generate_draft(
        self,
        topic: str,
        style_profile: Dict[str, Any],
        keywords: List[str],
        mode: Optional[str] = None,
        min_words: int = 1500,
        max_words: int = 2500
    ) -> str:
        """
        Generate initial draft content with structural diversity.
        """
        if not self.llm or not self.llm.is_available():
            return self._fallback_draft(topic, keywords)
        
        # Select dynamic structure and hook
        selected_mode = mode if mode in self.STRUCTURAL_MODES else random.choice(list(self.STRUCTURAL_MODES.keys()))
        mode_desc = self.STRUCTURAL_MODES[selected_mode]
        selected_hook = random.choice(self.OPENING_HOOKS)
        
        expressions_str = ", ".join(style_profile.get("expressions", [])[:10])
        keywords_str = ", ".join(keywords[:12])
        
        prompt = f"""Write a blog post about: {topic}

STRUCTURAL INTENT (ANTI-TEMPLATE):
- Mode: {selected_mode} ({mode_desc})
- Hook Style: {selected_hook}
- PROHIBITION: Do NOT use a fixed 'Intro -> Point 1 -> Point 2 -> Conclusion' layout. 
- PROHIBITION: Do NOT use repetitive H2 headings in predictable places.
- GUIDELINE: Follow the organic flow of your thoughts as Javi Pas.

STYLE REQUIREMENTS:
- Tone: {style_profile.get('tone', 'conversational and personal')}
- Voice: first person (Javi Pas)
- Expressions to use: {expressions_str}
- Related keywords: {keywords_str}

CONTENT GUIDELINES:
- Length: {min_words}-{max_words} words (approximate)
- Start with the selected HOOK STYLE.
- Use short-medium paragraphs mixed with single-sentence emphasis.
- Add occasional parentheses for clarifications (asides).
- Share personal experiments or 'cacharreo'.
- Mention your family/miniresort if it fits the narrative.
- End with a question or a call to comments but NO standard 'Conclusión' heading.
- Use markdown format (# for title, and use ## only if strictly necessary for flow).

Write a complete, organic, and spontaneous blog post. Use only markdown."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are Javi Pas, the famous Spanish tech blogger. You hate SEO-optimized boring templates. You write with soul, humor, and a bit of 'cacharreo' nostalgia. Your structure is unpredictable and organic.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(
                messages,
                temperature=0.85,
                max_tokens=3500
            )
            
            return response.content
            
        except Exception as e:
            logger.warning("Content generation failed: %s. Using fallback.", e)
            return self._fallback_draft(topic, keywords)

    def refine_content(
        self,
        draft: str,
        critique_feedback: Dict[str, Any],
        style_profile: Dict[str, Any]
    ) -> str:
        """
        Refine content based on critique feedback while preserving organic structure.
        """
        if not self.llm or not self.llm.is_available():
            return draft
        
        suggestions = critique_feedback.get('suggestions', [])
        suggestions_str = "\n".join(f"- {s}" for s in suggestions)
        
        prompt = f"""Refine this organic blog post.

ORIGINAL CONTENT:
{draft}

SUGGESTIONS FOR IMPROVEMENT:
{suggestions_str}

INSTRUCTIONS:
- CRITICAL: Maintain the unpredictable, organic structure. DO NOT normalize it into a template.
- Address the suggestions while keeping the 'Javi Pas' voice.
- Ensure the tone remains personal and conversational.
- Don't just add content; improve the flow.

Provide the refined version in markdown format."""

        try:
            messages = self.llm.create_messages(
                system_prompt="You are an editor specializing in maintaining unique author voices against generic AI templates.",
                user_prompt=prompt
            )
            
            response = self.llm.chat_completion(
                messages,
                temperature=0.7,
                max_tokens=3800
            )
            
            return response.content
            
        except Exception as e:
            logger.warning("Refinement failed: %s. Returning original draft.", e)
            return draft

    def _fallback_draft(self, topic: str, keywords: list) -> str:
        """Generate a basic draft when LLM is not available."""
        keywords_str = ", ".join(keywords[:5]) if keywords else "tecnología, cacharreo"
        return (
            f"# {topic}\n\n"
            f"A ver, que me habéis preguntado mucho por esto de {topic}. "
            "La verdad es que es un tema que me tiene enganchado, porque mezcla ilusión, "
            "herramientas reales y ese punto de experimentación que tanto nos gusta.\n\n"
            "Si me preguntas por una conclusión rápida, te diría que estamos en ese momento "
            "en el que todavía se puede aprender muchísimo probando cosas pequeñas, sin montar "
            "una infraestructura gigante. Lo importante no es solo el modelo, sino cómo encaja "
            "en tu flujo de trabajo diario y qué problemas concretos te resuelve.\n\n"
            f"En mi caso, cuando pienso en {topic}, siempre termino volviendo a lo mismo: "
            f"{keywords_str}. Si consigues aterrizar eso en ejemplos prácticos, el salto de valor "
            "es inmediato.\n\n"
            "Y ahora te lanzo la pregunta: ¿cómo lo estás integrando tú en tu día a día? "
            "Porque aquí es donde de verdad se separa el hype de lo que funciona."
        )

    def build_generation_record(
        self,
        topic: str,
        content: str,
        source_refs: Optional[List[str]] = None,
        category: str = "technology",
    ) -> Dict[str, Any]:
        """Build a normalized metadata record for generated content."""
        return {
            "topic": topic,
            "topic_category": category,
            "source_summary": source_refs or [],
            "word_count": len((content or "").split()),
        }

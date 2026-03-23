"""
Content Generator Agent.

Generates blog content in the style of the analyzed blogger.
Uses few-shot learning and style profiles extracted from corpus.
"""

from typing import Dict, Any, Optional, List
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
        self, api_key: Optional[str] = None, model: Optional[str] = None, provider: str = "auto"
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
        self.style_profile = None

        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model,
                    temperature=0.8,
                    max_tokens=3000,
                )
            except Exception as e:
                print(f"Warning: Failed to initialize LLM provider: {e}")
                self.llm = None
        else:
            self.llm = None

    def load_style_profile(self, profile_path: str):
        """Load style profile from JSON file."""
        import json

        with open(profile_path, "r", encoding="utf-8") as f:
            self.style_profile = json.load(f)
        return self.style_profile

    def set_style_profile(self, profile: Dict[str, Any]):
        """Set style profile directly."""
        self.style_profile = profile

    def generate_draft(
        self,
        topic: str,
        style_profile: Dict[str, Any] = None,
        keywords: list = None,
        min_words: int = 1500,
        max_words: int = 2500,
    ) -> str:
        """
        Generate initial draft content using few-shot learning.

        Args:
            topic: Topic to write about
            style_profile: Style profile (from StyleExtractor or StyleAnalyzer)
            keywords: Keywords from KeywordExtractor
            min_words: Minimum word count
            max_words: Maximum word count

        Returns:
            Draft content as markdown string
        """
        profile = style_profile or self.style_profile or {}

        if not self.llm or not self.llm.is_available():
            return self._fallback_draft(topic, keywords, profile)

        # Extraer elementos del perfil
        expressions = profile.get("expressions", [])[:10]
        vocabulary = profile.get("vocabulary", [])[:20]
        topics = profile.get("topics", [])
        tone = profile.get("tone", "coloquial y cercano")
        voice = profile.get("voice", "primera persona")
        sentence_pattern = profile.get("sentence_pattern", "oraciones de longitud media")
        paragraph_pattern = profile.get("paragraph_pattern", "párrafos de longitud media")
        use_of_humor = profile.get("use_of_humor", "humor irónico")
        technical_level = profile.get("technical_level", "técnico-intermedio")
        common_opens = profile.get("common_opens", [])[:2]
        common_closes = profile.get("common_closes", [])[:2]

        keywords_str = ", ".join(keywords[:15]) if keywords else ""

        # Few-shot examples
        few_shot_examples = ""
        if common_opens:
            few_shot_examples += f'\nEJEMPLO DE INTRODUCCIÓN (similar a cómo escribe el blogger):\n"{common_opens[0]}"\n'
        if common_closes:
            few_shot_examples += f'\nEJEMPLO DE CIERRE (similar a cómo termina los artículos):\n"{common_closes[0]}"\n'

        prompt = f"""Eres un blogger de tecnología español que escribe artículos en un estilo muy característico. Tu tarea es escribir un artículo completo sobre el tema indicado, imitando fielmente el estilo del blogger original.

TEMA DEL ARTÍCULO: {topic}

PERFIL DE ESTILO DEL BLOGGER:
- Tono: {tone}
- Voz: {voice}
- Patrón de oraciones: {sentence_pattern}
- Patrón de párrafos: {paragraph_pattern}
- Uso del humor: {use_of_humor}
- Nivel técnico: {technical_level}

VOCABULARIO CARACTERÍSTICO (usa estas palabras de forma natural):
{", ".join(vocabulary)}

EXPRESIONES TÍPICAS (incorpóralas naturalmente en el texto):
{", ".join(expressions)}

TEMS QUE SUELE TRATAR EL BLOGGER:
{", ".join(topics)}

{few_shot_examples}

REQUISITOS DEL ARTÍCULO:
- Longitud: entre {min_words} y {max_words} palabras
- Escribe en primera persona, como si lo estuvieras contando a un amigo
- Usa un tono {tone}, con cercanía y algo de humor
- Incluye alguna referencia personal o anéctdota si es natural
- Estructura el artículo con secciones (##)
- Termina con alguna pregunta o llamada a la acción para el lector
- Keywords a incluir naturalmente: {keywords_str}
- NO copies texto del blogger original, solo imita su ESTILO
- Usa markdown para estructurar (# títulos, ## secciones, negritas, etc.)

Escribe el artículo completo:"""

        try:
            messages = self.llm.create_messages(
                system_prompt="Eres un experto escribiendo artículos de tecnología en español, con un estilo cercano, humorístico y personal. Escribes como Javi Pas (javipas.com), un blogger conocido por su tono coloquial, sus expresiones características y su forma narrar experiencias personales.",
                user_prompt=prompt,
            )

            response = self.llm.chat_completion(messages, temperature=0.8, max_tokens=3500)

            return response.content

        except Exception as e:
            print(f"Warning: Content generation failed: {e}. Using fallback.")
            return self._fallback_draft(topic, keywords, profile)

    def refine_content(
        self, draft: str, critique_feedback: Dict[str, Any], style_profile: Dict[str, Any]
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

        suggestions = critique_feedback.get("suggestions", [])
        suggestions_str = "\\n".join(f"- {s}" for s in suggestions)

        prompt = f"""Refine this blog post based on the critique feedback.

ORIGINAL CONTENT:
{draft}

CRITIQUE FEEDBACK:
Coherence Score: {critique_feedback.get("coherence_score", "N/A")}/10
Style Match: {critique_feedback.get("style_match", "N/A")}/10

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
                user_prompt=prompt,
            )

            response = self.llm.chat_completion(messages, temperature=0.7, max_tokens=3500)

            return response.content

        except Exception as e:
            print(f"Warning: Refinement failed: {e}. Returning original draft.")
            return draft

    def _fallback_draft(
        self, topic: str, keywords: list = None, style_profile: Dict[str, Any] = None
    ) -> str:
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

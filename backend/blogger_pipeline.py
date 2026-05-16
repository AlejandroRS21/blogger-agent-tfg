"""
Pipeline completo: Investigar noticias actuales + Generar artículo con estilo de blogger.

Este script:
1. Busca noticias actuales sobre un tema
2. Usa el perfil de estilo de Javi Pas
3. Genera un artículo en ese estilo
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aphra_blogger.agents.news_research_agent import NewsResearchAgent
from aphra_blogger.agents.content_generator import ContentGenerator


class BlogGeneratorPipeline:
    """Pipeline completo para generar artículos sobre noticias actuales."""

    def __init__(self, style_profile_path: str = "javipas_style_profile.json"):
        # Cargar perfil de estilo
        if os.path.exists(style_profile_path):
            with open(style_profile_path, "r", encoding="utf-8") as f:
                self.style_profile = json.load(f)
            print(f"✓ Perfil de estilo cargado: {self.style_profile.get('alias', 'Unknown')}")
        else:
            print(f"⚠ Perfil no encontrado: {style_profile_path}")
            self.style_profile = {}

        # Inicializar agentes
        self.news_agent = NewsResearchAgent()
        self.content_generator = ContentGenerator()
        self.content_generator.style_profile = self.style_profile

    def generate_article(
        self, topic: str, include_news: bool = True, keywords: list = None
    ) -> dict:
        """
        Genera un artículo sobre un tema.

        Args:
            topic: Tema del artículo
            include_news: Si True, busca noticias actuales
            keywords: Keywords opcionales

        Returns:
            Dict con article, metadata y news context
        """
        news_context = ""
        articles_found = []

        if include_news:
            print(f"\n📰 Investigando noticias sobre: {topic}")
            news_result = self.news_agent.research_and_format_for_generation(topic)
            news_context = news_result["context"]
            articles_found = news_result["articles"]

            print(f"✓ {len(articles_found)} noticias encontradas")

            # Mostrar algunas noticias
            for i, art in enumerate(articles_found[:3], 1):
                print(f"  {i}. {art['title'][:60]}...")

        # Generar contenido
        print(f"\n✍️ Generando artículo en estilo {self.style_profile.get('alias', 'blogger')}...")

        # Crear prompt mejorado con noticias
        if news_context:
            enhanced_keywords = keywords or []
            for art in articles_found:
                # Extraer keywords de los títulos
                words = art["title"].split()
                enhanced_keywords.extend([w for w in words if len(w) > 4])

            content = self._generate_with_news(topic, news_context, enhanced_keywords)
        else:
            content = self.content_generator.generate_draft(
                topic=topic,
                keywords=keywords or [],
                blogger_urls=None
            )

        # Metadata
        word_count = len(content.split())

        result = {
            "topic": topic,
            "content": content,
            "word_count": word_count,
            "news_count": len(articles_found),
            "style_used": self.style_profile.get("alias", "Unknown"),
            "articles": articles_found,
            "generated_at": import_datetime_now(),
        }

        return result

    def _generate_with_news(self, topic: str, news_context: str, keywords: list) -> str:
        """Genera contenido incorporando las noticias."""

        alias = self.style_profile.get("alias", "el blogger")

        # Crear prompt con noticias
        prompt = f"""Eres {alias}, un blogger de tecnología español que escribe artículos sobre noticias actuales. Tu estilo es muy característico: cercano, con humor, y expresiones típicas.

CONTEXTO DE NOTICIAS ACTUALES:
{news_context}

TEMA DEL ARTÍCULO: {topic}

INSTRUCCIONES:
- Escribe un artículo completo (1500-2500 palabras) incorporando las noticias recientes
- Usa tu estilo característico: tono coloquial, humor sutil, expresiones como "me alucina", "dicho y hecho", "el caso es que", etc.
- Cuéntanos tu opinión personal sobre estas noticias
- Incluye alguna referencia personal si es natural
- Estructura el artículo con secciones (##)
- Termina preguntando a los lectores qué opinan
- NO copies las noticias, sino que das tu opinión y análisis
- Al final del post, agregá una línea de atribución: "Este post fue escrito al estilo de {alias}."

Usa este vocabulario característico: {", ".join(self.style_profile.get("vocabulary", [])[:20])}
Usa estas expresiones: {", ".join(self.style_profile.get("expressions", [])[:10])}

Escribe el artículo completo:"""

        # Intentar usar LLM
        if self.content_generator.llm and self.content_generator.llm.is_available():
            try:
                messages = self.content_generator.llm.create_messages(
                    system_prompt="Eres Javi Pas, blogger de tecnología español con estilo cercano y humorístico.",
                    user_prompt=prompt,
                )
                response = self.content_generator.llm.chat_completion(
                    messages, temperature=0.8, max_tokens=3500
                )
                return response.content
            except Exception as e:
                print(f"⚠ Error con LLM: {e}")

        # Fallback
        fallback = self.content_generator.generate_draft(topic, keywords=keywords, blogger_urls=None)
        return fallback

    def generate_sample_articles(self, topics: list = None):
        """Genera artículos de ejemplo."""
        if topics is None:
            topics = [
                "El futuro de la IA en móviles",
                "Apple vs Google: la guerra de la IA",
                "Tesla y los coches autónomos en 2026",
                "Por qué los Macs con IA van a cambiar todo",
                "Las nuevas funciones de ChatGPT",
            ]

        print("=" * 60)
        print("GENERANDO ARTÍCULOS DE EJEMPLO")
        print("=" * 60)

        for topic in topics:
            print(f"\n>>> {topic}")
            print("-" * 40)

            result = self.generate_article(topic)

            print(f"\n📝 Artículo generado ({result['word_count']} palabras)")
            print(f"   Noticias usadas: {result['news_count']}")
            print(f"   Estilo: {result['style_used']}")

            # Mostrar primeras líneas
            print("\n[Inicio del artículo]")
            print(result["content"][:500])
            print("...")

            # Guardar
            filename = topic.lower().replace(" ", "_")[:50] + ".json"
            with open(f"outputs/{filename}", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✓ Guardado en outputs/{filename}")

            print("\n" + "=" * 60)


def import_datetime_now():
    from datetime import datetime

    return datetime.now().isoformat()


def main():
    # Crear pipeline
    pipeline = BlogGeneratorPipeline()

    # Topics de prueba
    test_topics = [
        "Apple Intelligence 2026",
        "Elon Musk y Tesla en 2026",
        "ChatGPT y la IA generativa",
        "Google Gemini vs OpenAI",
    ]

    # Si hay argumentos, usar el primero como tema
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        print(f"\n🎯 Generando artículo sobre: {topic}\n")

        result = pipeline.generate_article(topic)

        print("\n" + "=" * 60)
        print("RESULTADO")
        print("=" * 60)
        print(f"\n📝 Artículo ({result['word_count']} palabras)")
        print(f"📰 Noticias incorporadas: {result['news_count']}")
        print(f"🎨 Estilo: {result['style_used']}")
        print("\n" + "-" * 60)
        print(result["content"])
        print("-" * 60)
    else:
        # Generar artículos de ejemplo
        pipeline.generate_sample_articles(test_topics)


if __name__ == "__main__":
    main()

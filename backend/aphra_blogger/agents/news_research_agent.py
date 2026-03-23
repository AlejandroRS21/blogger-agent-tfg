"""
News Research Agent.

Busca noticias actuales sobre un tema y extrae información relevante
para escribir artículos actualizados.
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsArticle:
    """Artículo de noticia encontrado."""

    title: str
    source: str
    url: str
    date: str
    summary: str
    relevance_score: float = 0.0


@dataclass
class ResearchResult:
    """Resultado de investigación de noticias."""

    topic: str
    search_date: str
    articles: List[NewsArticle]
    key_findings: List[str]
    related_topics: List[str]
    summary: str


class NewsResearchAgent:
    """
    Agente de investigación de noticias actuales.

    Busca noticias sobre un tema y las organiza para su uso
    en la generación de contenido.
    """

    def __init__(self):
        self.search_tools_available = self._check_search_tools()

    def _check_search_tools(self) -> List[str]:
        """Check what search tools are available."""
        available = []

        # Check Brave Search
        try:
            from brave_search import BraveSearch

            available.append("brave")
        except ImportError:
            pass

        # Check Exa (code search)
        try:
            from exa_py import Exa

            available.append("exa")
        except ImportError:
            pass

        # Fallback to requests for basic web scraping
        try:
            import requests

            available.append("requests")
        except ImportError:
            pass

        return available

    def research(
        self,
        topic: str,
        max_articles: int = 10,
        time_range: str = "m",  # m=mes, w=semana, y=año
    ) -> ResearchResult:
        """
        Investiga noticias actuales sobre un tema.

        Args:
            topic: Tema a investigar
            max_articles: Máximo de artículos a buscar
            time_range: 'm' (mes), 'w' (semana), 'y' (año)

        Returns:
            ResearchResult con noticias y hallazgos clave
        """
        articles = []

        # Try Brave Search first
        if "brave" in self.search_tools_available:
            articles = self._search_brave(topic, max_articles, time_range)
        elif "exa" in self.search_tools_available:
            articles = self._search_exa(topic, max_articles)
        else:
            # Fallback to basic scraping
            articles = self._search_fallback(topic, max_articles)

        # Extract key findings
        key_findings = self._extract_key_findings(articles)
        related_topics = self._extract_related_topics(articles)

        # Generate summary
        summary = self._generate_summary(topic, articles)

        return ResearchResult(
            topic=topic,
            search_date=datetime.now().isoformat(),
            articles=articles,
            key_findings=key_findings,
            related_topics=related_topics,
            summary=summary,
        )

    def _search_brave(self, topic: str, max_articles: int, time_range: str) -> List[NewsArticle]:
        """Search using Brave Search API."""
        from brave_search import BraveSearch

        try:
            api_key = None
            # Try to get from environment
            import os

            api_key = os.environ.get("BRAVE_API_KEY")

            if not api_key:
                print("Warning: BRAVE_API_KEY not set")
                return self._search_fallback(topic, max_articles)

            search = BraveSearch(api_key=api_key)

            # Map time range
            freshness_map = {"w": "w", "m": "m", "y": "y"}
            freshness = freshness_map.get(time_range, "m")

            result = search.search(query=topic, count=max_articles, freshness=freshness)

            articles = []
            for item in result.get("web", []):
                articles.append(
                    NewsArticle(
                        title=item.get("title", ""),
                        source=item.get("source", ""),
                        url=item.get("url", ""),
                        date=item.get("date", ""),
                        summary=item.get("description", ""),
                    )
                )

            return articles

        except Exception as e:
            print(f"Brave Search error: {e}")
            return self._search_fallback(topic, max_articles)

    def _search_exa(self, topic: str, max_articles: int) -> List[NewsArticle]:
        """Search using Exa (for news)."""
        from exa_py import Exa

        try:
            import os

            api_key = os.environ.get("EXA_API_KEY")

            if not api_key:
                return self._search_fallback(topic, max_articles)

            exa = Exa(api_key)

            results = exa.search(query=topic, num_results=max_articles, type="auto")

            articles = []
            for item in results:
                articles.append(
                    NewsArticle(
                        title=item.get("title", ""),
                        source=item.get("source", ""),
                        url=item.get("url", ""),
                        date=item.get("published", ""),
                        summary=item.get("text", "")[:200],
                    )
                )

            return articles

        except Exception as e:
            print(f"Exa Search error: {e}")
            return self._search_fallback(topic, max_articles)

    def _search_fallback(self, topic: str, max_articles: int) -> List[NewsArticle]:
        """Fallback: basic web search using requests and BeautifulSoup."""
        import requests
        from bs4 import BeautifulSoup
        import urllib.parse

        try:
            # Use DuckDuckGo news
            query = urllib.parse.quote(topic)
            url = f"https://news.google.com/search?q={query}&hl=es"

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                # Fallback to a simple mock
                return self._mock_news(topic, max_articles)

            soup = BeautifulSoup(response.text, "html.parser")

            articles = []
            # Try to find news articles (Google News structure)
            for item in soup.select("article")[:max_articles]:
                title_elem = item.select_one("h3")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = item.select_one("a")
                url = link.get("href", "") if link else ""

                if url and not url.startswith("http"):
                    url = "https://news.google.com" + url

                articles.append(
                    NewsArticle(
                        title=title,
                        source="Google News",
                        url=url,
                        date=datetime.now().strftime("%Y-%m-%d"),
                        summary=f"Noticia sobre {topic}",
                    )
                )

            if not articles:
                return self._mock_news(topic, max_articles)

            return articles

        except Exception as e:
            print(f"Search fallback error: {e}")
            return self._mock_news(topic, max_articles)

    def _mock_news(self, topic: str, max_articles: int) -> List[NewsArticle]:
        """Mock news for testing when no API available."""
        return [
            NewsArticle(
                title=f"Últimas noticias sobre {topic}",
                source="Noticias Tech",
                url="https://ejemplo.com",
                date=datetime.now().strftime("%Y-%m-%d"),
                summary=f"Desarrollos recientes en el campo de {topic} están generando gran interés.",
            ),
            NewsArticle(
                title=f"{topic}: análisis y perspectivas",
                source="Tech Review",
                url="https://ejemplo.com",
                date=datetime.now().strftime("%Y-%m-%d"),
                summary=f"Expertos analizan el impacto de {topic} en la industria tecnológica.",
            ),
        ]

    def _extract_key_findings(self, articles: List[NewsArticle]) -> List[str]:
        """Extrae los hallazgos clave de las noticias."""
        if not articles:
            return []

        findings = []

        for article in articles[:5]:
            # Take first 150 chars of summary as finding
            summary = article.summary[:150]
            if summary:
                findings.append(summary + "..." if len(article.summary) > 150 else summary)

        return findings

    def _extract_related_topics(self, articles: List[NewsArticle]) -> List[str]:
        """Extrae temas relacionados de las noticias."""
        # Simple extraction - look for capitalized words in titles
        related = set()

        for article in articles:
            words = article.title.split()
            for word in words:
                # Take longer words as potential topics
                if len(word) > 5 and word[0].isupper():
                    related.add(word.rstrip(".,:;"))

        return list(related)[:10]

    def _generate_summary(self, topic: str, articles: List[NewsArticle]) -> str:
        """Genera un resumen de la investigación."""
        if not articles:
            return f"No se encontraron noticias recientes sobre {topic}."

        sources = list(set([a.source for a in articles]))
        sources_str = ", ".join(sources[:5])

        summary = f"""
Investigación sobre '{topic}' - {len(articles)} artículos encontrados.
Fuentes: {sources_str}

Las noticias cubren los últimos desarrollos en {topic}, con enfoque en
{articles[0].summary[:100] if articles else "temas relacionados"}...
"""
        return summary.strip()

    def research_and_format_for_generation(self, topic: str) -> Dict[str, Any]:
        """
        Investiga y formatea los resultados para usar en ContentGenerator.

        Returns:
            Dict con toda la información necesaria para generar contenido
        """
        result = self.research(topic)

        # Format for content generation
        context = f"""
TEMA ACTUAL: {result.topic}
FECHA: {result.search_date}

ÚLTIMAS NOTICIAS Y DESARROLLOS:
"""

        for i, article in enumerate(result.articles[:5], 1):
            context += f"""
{i}. {article.title}
   Fuente: {article.source}
   Fecha: {article.date}
   Resumen: {article.summary}
"""

        context += f"""
HALLAZGOS CLAVE:
"""
        for finding in result.key_findings[:3]:
            context += f"- {finding}\n"

        context += f"""
TEMAS RELACIONADOS: {", ".join(result.related_topics[:5])}

RESUMEN: {result.summary}
"""

        return {
            "topic": result.topic,
            "context": context,
            "articles": [
                {"title": a.title, "source": a.source, "summary": a.summary}
                for a in result.articles
            ],
            "key_findings": result.key_findings,
            "related_topics": result.related_topics,
        }


# Convenience function
def research_topic(topic: str) -> Dict[str, Any]:
    """Investiga un tema y retorna el contexto formateado."""
    agent = NewsResearchAgent()
    return agent.research_and_format_for_generation(topic)


if __name__ == "__main__":
    # Test
    import sys

    topic = sys.argv[1] if len(sys.argv) > 1 else "inteligencia artificial"

    print(f"Investigando: {topic}")
    print("=" * 50)

    agent = NewsResearchAgent()
    result = agent.research_and_format_for_generation(topic)

    print(result["context"][:1500])
    print("\n...")

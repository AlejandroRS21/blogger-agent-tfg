"""
Research Agent.

Performs web searches to provide context and up-to-date information for blog posts.
"""

from typing import Dict, Any, List, Optional
import os
import requests
import json
from datetime import datetime, timezone

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


class ResearchAgent:
    """
    Performs web searches and summarizes research for blog content.
    
    Identifies:
    - Current facts and figures
    - Related news and events
    - Key terminology
    - Supporting evidence
    
    Uses Brave Search API if BRAVE_API_KEY is available in .env.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto",
        brave_api_key: Optional[str] = None
    ):
        """
        Initialize the ResearchAgent.
        
        Args:
            api_key: API key for LLM provider
            model: Model to use for summarization.
            provider: LLM provider
            brave_api_key: Brave Search API Key
        """
        self.model = model
        self.provider_name = provider
        self.brave_api_key = brave_api_key or os.getenv("BRAVE_API_KEY")
        
        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model
                )
            except Exception as e:
                print(f"⚠️ Error initializing ResearchAgent LLM: {e}")
                self.llm = None
        else:
            self.llm = None

    def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Performs a web search using Brave Search API.
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            Dictionary with results and status
        """
        if not self.brave_api_key:
            return {
                "status": "No API Key",
                "results": [],
                "summary": "No se proporcionó BRAVE_API_KEY para investigación en tiempo real."
            }
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.brave_api_key
        }
        
        try:
            url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count={limit}&lang=es"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant info
            results = []
            if "web" in data and "results" in data["web"]:
                for res in data["web"]["results"]:
                    results.append({
                        "title": res.get("title"),
                        "description": res.get("description"),
                        "url": res.get("url")
                    })
            
            return {
                "status": "OK",
                "results": results,
                "summary": self._summarize(query, results) if results else "No se encontraron resultados relevantes."
            }
        except Exception as e:
            return {
                "status": "Error",
                "results": [],
                "summary": f"Error al buscar en la web: {str(e)}"
            }

    def _summarize(self, topic: str, results: List[Dict[str, str]]) -> str:
        """Summarizes search results using the LLM."""
        if not self.llm:
            return "\n".join([f"- {r['title']}: {r['description']}" for r in results])
        
        prompt = f"""
        Como un Agente de Investigación experto, resume los siguientes resultados de búsqueda web sobre el tema: "{topic}".
        Extrae los datos más relevantes, hechos recientes y cifras importantes que puedan servir como contexto para escribir un blog.
        Mantén el resumen conciso y estructurado.

        Resultados:
        {json.dumps(results, indent=2, ensure_ascii=False)}

        Resumen de investigación:
        """
        
        try:
            return self.llm.generate(prompt)
        except Exception as e:
            print(f"⚠️ Error in summarization: {e}")
            return "\n".join([f"- {r['title']}: {r['description']}" for r in results])

    def fetch_topic_candidates(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch topic candidates from web API with RSS/static fallback."""
        candidates: List[Dict[str, Any]] = []
        search_result = self.search(query=query, limit=limit)
        if search_result.get("status") == "OK":
            for item in search_result.get("results", []):
                candidates.append(
                    {
                        "title": item.get("title", "Untitled"),
                        "category": "technology",
                        "source": item.get("url", "brave"),
                        "published_at": datetime.now(timezone.utc),
                        "description": item.get("description", ""),
                    }
                )

        # RSS/static fallback for resilience.
        if not candidates:
            fallback_topics = [
                "Novedades de IA aplicada en desarrollo de software",
                "Tendencias de hardware para inferencia local",
                "Cambios recientes en ecosistemas de agentes LLM",
            ]
            for topic in fallback_topics[:limit]:
                candidates.append(
                    {
                        "title": topic,
                        "category": "technology",
                        "source": "fallback-rss",
                        "published_at": datetime.now(timezone.utc),
                        "description": "Fallback candidate generated without external API key.",
                    }
                )

        return candidates

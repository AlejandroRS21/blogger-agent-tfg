"""
Unsplash Image Search Agent.

Searches for relevant, high-quality photographs based on topic/prompt keywords.
Free tier: 50 requests/hour, no API key required for search with Client-ID header.
"""

import os
import re
from typing import List, Dict, Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


UNSPLASH_API = "https://api.unsplash.com/search/photos"


def _extract_keywords(prompt: str, max_words: int = 5) -> str:
    """Extract meaningful search keywords from an image prompt."""
    # Strip common filler phrases
    cleaned = re.sub(
        r'(professional|modern|hero image|illustrative|representing|about|related to|'
        r'high quality|clean design|technology theme|16:9 aspect ratio|'
        r'eye-catching|stunning|beautiful|amazing|inspiring|style|concept)',
        '', prompt, flags=re.IGNORECASE
    )
    # Take first N meaningful words
    words = [w for w in cleaned.split() if len(w) > 2][:max_words]
    return ' '.join(words) if words else prompt.split()[:max_words]


def search_image(query: str, access_key: Optional[str] = None) -> Optional[str]:
    """
    Search Unsplash for a photo matching the query.
    
    Args:
        query: Search keywords
        access_key: Unsplash API access key (falls back to env var)
        
    Returns:
        URL of the best matching photo, or None
    """
    if not REQUESTS_AVAILABLE:
        return None

    key = access_key or os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return None

    keywords = _extract_keywords(query)
    if not keywords:
        return None

    try:
        resp = requests.get(
            UNSPLASH_API,
            headers={"Authorization": f"Client-ID {key}"},
            params={"query": keywords, "per_page": 1, "orientation": "landscape"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if results:
            return results[0]["urls"]["regular"]
    except Exception as e:
        print(f"[Unsplash] Search failed for '{keywords}': {e}")

    return None


def enrich_images(prompts: List[Dict[str, str]], access_key: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Take image prompt dicts (from ImageSelectorAgent) and add Unsplash URLs.
    
    Each prompt dict gets a 'url' field with a real photo URL.
    Prompts that already have a 'url' are skipped.
    """
    enriched = []
    for img in prompts:
        if img.get("url"):
            enriched.append(img)
            continue

        # Try the prompt first, fall back to alt_text
        query = img.get("prompt", "") or img.get("alt_text", "")
        url = search_image(query, access_key)

        if url:
            img["url"] = url
            img["source"] = "unsplash"
            print(f"[Unsplash] ✓ Image for '{query[:40]}...' -> {url[:60]}...")
        else:
            print(f"[Unsplash] ✗ No result for '{query[:40]}...'")

        enriched.append(img)

    return enriched

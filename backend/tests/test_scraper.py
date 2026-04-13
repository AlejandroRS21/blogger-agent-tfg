"""Tests for blog scraper."""

import pytest
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import Mock
import requests
from tools.scraper import BlogScraper, BlogPost, scrape_javipas
from src.orchestrator.continuous.topic_selector import TopicCandidate, TopicSelector
from src.orchestrator.continuous.source_guard import SourceGuard
from aphra_blogger.agents.research_agent import ResearchAgent

# Mock data for testing
MOCK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Post - Test Blog</title>
</head>
<body>
    <article>
        <h1 class="entry-title">Test Blog Post Title</h1>
        <span class="author">Test Author</span>
        <time datetime="2026-02-10">February 10, 2026</time>
        
        <div class="entry-content">
            <p>This is the first paragraph of the test post.</p>
            <p>This is the second paragraph with more content.</p>
            <p>And a third paragraph to make it realistic.</p>
        </div>
        
        <div class="tags">
            <a rel="tag" href="/tag/test">test</a>
            <a rel="tag" href="/tag/python">python</a>
        </div>
    </article>
</body>
</html>
"""

MOCK_LISTING_HTML = """
<!DOCTYPE html>
<html>
<body>
    <article>
        <h2 class="entry-title"><a href="https://example.com/post1">Post 1</a></h2>
    </article>
    <article>
        <h2 class="entry-title"><a href="https://example.com/post2">Post 2</a></h2>
    </article>
    <article>
        <h2 class="entry-title"><a href="https://example.com/post3">Post 3</a></h2>
    </article>
</body>
</html>
"""


class TestBlogPost:
    """Tests for BlogPost dataclass."""
    
    def test_blog_post_creation(self):
        """Test creating a BlogPost."""
        post = BlogPost(
            url="https://example.com/test",
            title="Test Post",
            content="This is test content with multiple words here."
        )
        
        assert post.url == "https://example.com/test"
        assert post.title == "Test Post"
        assert post.content == "This is test content with multiple words here."
        assert post.word_count == 8  # Auto-calculated
        assert post.scraped_at is not None
    
    def test_blog_post_word_count(self):
        """Test automatic word count calculation."""
        content = "One two three four five"
        post = BlogPost(url="test", title="Test", content=content)
        
        assert post.word_count == 5
    
    def test_blog_post_with_metadata(self):
        """Test BlogPost with full metadata."""
        post = BlogPost(
            url="https://example.com/test",
            title="Test",
            content="Content",
            author="Jane Doe",
            date="2026-02-10",
            tags=["test", "python"],
            categories=["Tech"]
        )
        
        assert post.author == "Jane Doe"
        assert len(post.tags) == 2
        assert len(post.categories) == 1


class TestBlogScraper:
    """Tests for BlogScraper (without actual HTTP requests)."""
    
    def test_scraper_initialization(self):
        """Test scraper initialization."""
        scraper = BlogScraper(
            base_url="https://example.com",
            delay=1.0,
            max_posts=10
        )
        
        assert scraper.base_url == "https://example.com"
        assert scraper.delay == 1.0
        assert scraper.max_posts == 10
    
    def test_scraper_url_normalization(self):
        """Test that trailing slashes are removed."""
        scraper = BlogScraper(base_url="https://example.com/")
        assert scraper.base_url == "https://example.com"
    
    def test_get_page_url(self):
        """Test pagination URL generation."""
        scraper = BlogScraper(base_url="https://example.com")
        
        assert scraper._get_page_url(1) == "https://example.com"
        assert scraper._get_page_url(2) == "https://example.com/page/2/"
        assert scraper._get_page_url(5) == "https://example.com/page/5/"
    
    def test_extract_title(self):
        """Test title extraction from HTML."""
        from bs4 import BeautifulSoup
        
        scraper = BlogScraper(base_url="https://example.com")
        soup = BeautifulSoup(MOCK_HTML, 'html.parser')
        
        title = scraper._extract_title(soup)
        assert title == "Test Blog Post Title"
    
    def test_extract_content(self):
        """Test content extraction from HTML."""
        from bs4 import BeautifulSoup
        
        scraper = BlogScraper(base_url="https://example.com")
        soup = BeautifulSoup(MOCK_HTML, 'html.parser')
        
        content = scraper._extract_content(soup)
        assert "first paragraph" in content
        assert "second paragraph" in content
        assert "third paragraph" in content
    
    def test_extract_author(self):
        """Test author extraction."""
        from bs4 import BeautifulSoup
        
        scraper = BlogScraper(base_url="https://example.com")
        soup = BeautifulSoup(MOCK_HTML, 'html.parser')
        
        author = scraper._extract_author(soup)
        assert author == "Test Author"
    
    def test_extract_tags(self):
        """Test tag extraction."""
        from bs4 import BeautifulSoup
        
        scraper = BlogScraper(base_url="https://example.com")
        soup = BeautifulSoup(MOCK_HTML, 'html.parser')
        
        tags = scraper._extract_tags(soup)
        assert len(tags) == 2
        assert "test" in tags
        assert "python" in tags
    
    def test_extract_post_links(self):
        """Test extracting post URLs from listing page."""
        from bs4 import BeautifulSoup
        
        scraper = BlogScraper(base_url="https://example.com")
        soup = BeautifulSoup(MOCK_LISTING_HTML, 'html.parser')
        
        urls = scraper._extract_post_links(soup)
        assert len(urls) == 3
        assert "https://example.com/post1" in urls
        assert "https://example.com/post2" in urls
        assert "https://example.com/post3" in urls


class TestCorpusIO:
    """Tests for saving and loading corpus."""
    
    def test_save_and_load_corpus(self, tmp_path):
        """Test saving and loading corpus to/from JSON."""
        # Create test posts
        posts = [
            BlogPost(
                url="https://example.com/post1",
                title="Post 1",
                content="Content of post 1",
                author="Author 1",
                tags=["tag1", "tag2"]
            ),
            BlogPost(
                url="https://example.com/post2",
                title="Post 2",
                content="Content of post 2",
                author="Author 2"
            )
        ]
        
        # Save corpus
        scraper = BlogScraper(base_url="https://example.com")
        output_file = tmp_path / "test_corpus.json"
        scraper.save_corpus(posts, str(output_file))
        
        # Verify file exists
        assert output_file.exists()
        
        # Load corpus
        loaded_posts = BlogScraper.load_corpus(str(output_file))
        
        # Verify loaded data
        assert len(loaded_posts) == 2
        assert loaded_posts[0].title == "Post 1"
        assert loaded_posts[1].title == "Post 2"
        assert loaded_posts[0].author == "Author 1"
    
    def test_corpus_metadata(self, tmp_path):
        """Test that corpus file includes metadata."""
        posts = [
            BlogPost(url="test", title="Test", content="Content")
        ]
        
        scraper = BlogScraper(base_url="https://example.com")
        output_file = tmp_path / "test_corpus.json"
        scraper.save_corpus(posts, str(output_file))
        
        # Load raw JSON
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        # Check metadata
        assert 'blog_url' in data
        assert 'scraped_at' in data
        assert 'post_count' in data
        assert 'total_words' in data
        assert data['post_count'] == 1
        assert data['blog_url'] == "https://example.com"


class TestIntegration:
    """Integration tests (these would need mocking for actual HTTP)."""
    
    @pytest.mark.skip(reason="Requires actual HTTP requests")
    def test_scrape_javipas_integration(self, tmp_path):
        """
        Integration test for scraping javipas.com.
        Skipped by default to avoid actual HTTP requests.
        """
        output_file = tmp_path / "javipas_test.json"
        
        posts = scrape_javipas(
            max_posts=5,
            output_file=str(output_file)
        )
        
        assert len(posts) > 0
        assert output_file.exists()
        
        # Verify posts have content
        for post in posts:
            assert post.title
            assert post.content
            assert post.word_count > 0


class TestTopicSelection:
    """Tests for recency and diversity in topic selection."""

    def test_select_prefers_recent_candidate(self):
        selector = TopicSelector(recency_window_hours=72)
        now = datetime.now(timezone.utc)
        candidates = [
            TopicCandidate("old", "ai", "x", published_at=now - timedelta(hours=70)),
            TopicCandidate("new", "ai", "x", published_at=now - timedelta(hours=2)),
        ]
        selected = selector.select(candidates)
        assert selected is not None
        assert selected.title == "new"

    def test_select_applies_diversity_boost(self):
        selector = TopicSelector(recency_window_hours=72, category_cooldown=1)
        now = datetime.now(timezone.utc)
        first = selector.select([TopicCandidate("a", "ai", "x", published_at=now)])
        assert first is not None
        second = selector.select(
            [
                TopicCandidate("same", "ai", "x", published_at=now),
                TopicCandidate("different", "cloud", "x", published_at=now - timedelta(hours=1)),
            ]
        )
        assert second is not None
        assert second.category == "cloud"


class TestSourceFallback:
    """Tests for multi-source fallback and source exhaustion handling."""

    def test_research_agent_fallback_without_api_key(self):
        agent = ResearchAgent(brave_api_key=None)
        topics = agent.fetch_topic_candidates(query="novedades ia", limit=3)
        assert len(topics) > 0
        assert topics[0]["source"] in {"fallback-rss", "brave"}

    def test_source_guard_detects_source_exhausted(self):
        guard = SourceGuard(allowed_domains=("api.search.brave.com", "fallback-rss"))
        sanitized = guard.sanitize_candidates(
            [
                {"title": "x", "source": "https://unknown.example", "description": "d"},
                {"title": "y", "source": "https://another.bad", "description": "d"},
            ]
        )
        assert sanitized == []

    def test_research_search_handles_timeout(self, monkeypatch):
        agent = ResearchAgent(brave_api_key="token")

        def _raise_timeout(*args, **kwargs):
            raise requests.Timeout("timeout")

        monkeypatch.setattr("aphra_blogger.agents.research_agent.requests.get", _raise_timeout)
        result = agent.search("novedades ia", limit=3)
        assert result["status"] == "Error"

    def test_research_search_handles_http_429(self, monkeypatch):
        agent = ResearchAgent(brave_api_key="token")
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("429 Too Many Requests")
        monkeypatch.setattr("aphra_blogger.agents.research_agent.requests.get", lambda *args, **kwargs: response)
        result = agent.search("novedades ia", limit=3)
        assert result["status"] == "Error"
        assert "429" in result["summary"]

    def test_research_search_handles_http_5xx(self, monkeypatch):
        agent = ResearchAgent(brave_api_key="token")
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
        monkeypatch.setattr("aphra_blogger.agents.research_agent.requests.get", lambda *args, **kwargs: response)
        result = agent.search("novedades ia", limit=3)
        assert result["status"] == "Error"
        assert "503" in result["summary"]

    def test_fetch_topic_candidates_fallback_on_malformed_payload(self, monkeypatch):
        agent = ResearchAgent(brave_api_key="token")
        monkeypatch.setattr(
            agent,
            "search",
            lambda query, limit=10: {"status": "OK", "results": [], "summary": "malformed"},
        )
        candidates = agent.fetch_topic_candidates(query="ai", limit=3)
        assert len(candidates) > 0
        assert all(c["source"] == "fallback-rss" for c in candidates)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

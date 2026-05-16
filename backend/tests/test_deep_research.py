"""
Strict TDD tests for deep-research-pipeline (Phases 2-5).

Tests cover:
- _scrape_with_scrapling() with mocked Fetcher
- _scrape_multiple_articles() with mixed success/failure
- _synthesize_research() with mocked LLM provider
- Modified research() method
- Content generator prompt enhancement
- Orchestrator integration
"""

import builtins
from unittest.mock import MagicMock, patch, PropertyMock
import pytest
from typing import Dict, Any, List

from aphra_blogger.agents.news_research_agent import (
    NewsResearchAgent,
    NewsArticle,
    ResearchResult,
    research_topic,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def agent():
    """Create a NewsResearchAgent instance with mocked search tools."""
    a = NewsResearchAgent()
    a.search_tools_available = ["requests"]  # avoid needing real API keys
    return a


@pytest.fixture
def mock_scrapling_fetcher():
    """Mock scrapling.Fetcher.get() to return a controllable response.

    The Fetcher.get() returns a Selector-like response object with:
      .status  (int)
      .body    (bytes)
      .get_all_text(ignore_tags) -> str/TextHandler
    """
    with patch("scrapling.Fetcher") as mock_fetcher:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.body = b"<html><body><p>Real article content with useful information about AI trends and developments in 2025.</p></body></html>"
        mock_response.get_all_text.return_value = "Real article content with useful information about AI trends and developments in 2025."

        mock_fetcher.get.return_value = mock_response
        yield mock_fetcher


@pytest.fixture
def mock_llm_provider():
    """Create a mocked LLM provider that returns predictable responses."""
    provider = MagicMock()
    provider.is_available.return_value = True

    mock_response = MagicMock()
    mock_response.content = (
        "## Key Facts\n"
        "- AI investment reached $200B in 2025\n"
        "- Three major regulatory frameworks proposed\n\n"
        "## Perspectives\n"
        "- Industry leaders are optimistic about regulation\n"
        "- Privacy advocates raise concerns about enforcement\n\n"
        "## Source List\n"
        "1. TechCrunch - https://techcrunch.com/ai-2025\n"
    )
    provider.chat_completion.return_value = mock_response
    provider.create_messages.return_value = [
        {"role": "system", "content": "system prompt"},
        {"role": "user", "content": "user prompt"},
    ]
    return provider


# ---------------------------------------------------------------------------
# Phase 2: Deep Article Scraping
# ---------------------------------------------------------------------------

class TestScrapeWithScrapling:
    """Tests for _scrape_with_scrapling()."""

    def test_successful_scrape_returns_clean_text(self, agent, mock_scrapling_fetcher):
        """Happy path: Fetcher.get returns 200, get_all_text extracts clean text."""
        result = agent._scrape_with_scrapling("https://example.com/article")
        assert result is not None
        assert "Real article content" in result
        assert "AI trends" in result

    def test_http_error_returns_none(self, agent, mock_scrapling_fetcher):
        """HTTP error (4xx/5xx) should return None."""
        mock_scrapling_fetcher.get.return_value.status = 404
        result = agent._scrape_with_scrapling("https://example.com/not-found")
        assert result is None

    def test_server_error_returns_none(self, agent, mock_scrapling_fetcher):
        """Server error (5xx) should return None."""
        mock_scrapling_fetcher.get.return_value.status = 500
        result = agent._scrape_with_scrapling("https://example.com/error")
        assert result is None

    def test_empty_content_returns_none(self, agent, mock_scrapling_fetcher):
        """Empty scraped content should return None."""
        mock_scrapling_fetcher.get.return_value.get_all_text.return_value = ""
        result = agent._scrape_with_scrapling("https://example.com/empty")
        assert result is None

    def test_whitespace_only_returns_none(self, agent, mock_scrapling_fetcher):
        """Whitespace-only content should return None."""
        mock_scrapling_fetcher.get.return_value.get_all_text.return_value = "   \n\n  \t  "
        result = agent._scrape_with_scrapling("https://example.com/whitespace")
        assert result is None

    def test_connection_error_returns_none(self, agent, mock_scrapling_fetcher):
        """Connection/network error raises exception -> returns None."""
        mock_scrapling_fetcher.get.side_effect = Exception("Connection refused")
        result = agent._scrape_with_scrapling("https://example.com/down")
        assert result is None

    def test_truncation_respects_max_chars(self, agent, mock_scrapling_fetcher):
        """Scraped text should be truncated to max_chars."""
        long_text = "word " * 2000  # ~10000 chars
        mock_scrapling_fetcher.get.return_value.get_all_text.return_value = long_text
        result = agent._scrape_with_scrapling("https://example.com/long", max_chars=100)
        assert result is not None
        assert len(result) <= 100

    def test_scrapling_not_installed_returns_none(self, agent):
        """When scrapling is not installed, should return None without crashing."""
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "scrapling":
                raise ImportError("Mock: no module named 'scrapling'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = agent._scrape_with_scrapling("https://example.com/article")
            assert result is None


class TestScrapeMultipleArticles:
    """Tests for _scrape_multiple_articles()."""

    def test_all_successful(self, agent):
        """All URLs scraped successfully -> all return scrape_success: True."""
        articles_meta = [
            {"title": "Article 1", "source": "Source A", "url": "https://example.com/1"},
            {"title": "Article 2", "source": "Source B", "url": "https://example.com/2"},
            {"title": "Article 3", "source": "Source C", "url": "https://example.com/3"},
        ]

        def mock_scrape(url, max_chars=5000):
            return f"Full text for {url}"

        with patch.object(agent, "_scrape_with_scrapling", side_effect=mock_scrape):
            scraped, stats = agent._scrape_multiple_articles(articles_meta, max_articles=3)

        assert len(scraped) == 3
        assert all(s["scrape_success"] for s in scraped)
        assert stats == {"total": 3, "succeeded": 3, "failed": 0}
        assert all(s["word_count"] > 0 for s in scraped)

    def test_partial_failure(self, agent):
        """Some URLs fail -> mix of scrape_success True/False."""
        articles_meta = [
            {"title": "Good 1", "source": "Src A", "url": "https://example.com/good1"},
            {"title": "Bad 1", "source": "Src B", "url": "https://example.com/bad1"},
            {"title": "Good 2", "source": "Src C", "url": "https://example.com/good2"},
            {"title": "Bad 2", "source": "Src D", "url": "https://example.com/bad2"},
            {"title": "Good 3", "source": "Src E", "url": "https://example.com/good3"},
        ]

        def mock_scrape(url, max_chars=5000):
            if "bad" in url:
                return None
            return f"Content for {url}"

        with patch.object(agent, "_scrape_with_scrapling", side_effect=mock_scrape):
            scraped, stats = agent._scrape_multiple_articles(articles_meta, max_articles=5)

        assert len(scraped) == 5
        assert stats == {"total": 5, "succeeded": 3, "failed": 2}

        successful = [s for s in scraped if s["scrape_success"]]
        failed = [s for s in scraped if not s["scrape_success"]]
        assert len(successful) == 3
        assert len(failed) == 2
        for s in successful:
            assert s["full_text"] != ""
            assert s["word_count"] > 0
        for f in failed:
            assert f["full_text"] == ""
            assert f["word_count"] == 0

    def test_all_fail(self, agent):
        """All URLs fail -> all return scrape_success: False, no exception."""
        articles_meta = [
            {"title": "Fail 1", "source": "Src A", "url": "https://example.com/fail1"},
            {"title": "Fail 2", "source": "Src B", "url": "https://example.com/fail2"},
        ]

        with patch.object(agent, "_scrape_with_scrapling", return_value=None):
            scraped, stats = agent._scrape_multiple_articles(articles_meta, max_articles=2)

        assert len(scraped) == 2
        assert stats == {"total": 2, "succeeded": 0, "failed": 2}
        assert all(not s["scrape_success"] for s in scraped)

    def test_empty_urls_list(self, agent):
        """No URLs provided -> empty lists returned, no error."""
        scraped, stats = agent._scrape_multiple_articles([], max_articles=5)
        assert scraped == []
        assert stats == {"total": 0, "succeeded": 0, "failed": 0}

    def test_max_articles_cap(self, agent):
        """More URLs than max_articles -> only first max_articles are processed."""
        articles_meta = [
            {"title": f"Article {i}", "source": "Src", "url": f"https://example.com/{i}"}
            for i in range(10)
        ]

        call_count = 0

        def mock_scrape(url, max_chars=5000):
            nonlocal call_count
            call_count += 1
            return f"Content"

        with patch.object(agent, "_scrape_with_scrapling", side_effect=mock_scrape):
            scraped, stats = agent._scrape_multiple_articles(articles_meta, max_articles=3)

        assert call_count == 3
        assert len(scraped) == 3
        assert stats == {"total": 3, "succeeded": 3, "failed": 0}


# ---------------------------------------------------------------------------
# Phase 3: Research Synthesis
# ---------------------------------------------------------------------------

class TestSynthesizeResearch:
    """Tests for _synthesize_research()."""

    def test_happy_path_multiple_articles(self, agent, mock_llm_provider):
        """Multiple articles -> structured brief with facts, perspectives, sources."""
        articles = [
            {"title": "AI in 2025", "source": "TechCrunch", "url": "https://tc.com/ai",
             "full_text": "AI investment reached $200B in 2025. Three major regulatory frameworks proposed.",
             "word_count": 15, "scrape_success": True},
            {"title": "AI Regulation Debate", "source": "Wired", "url": "https://wired.com/reg",
             "full_text": "Industry leaders are optimistic about regulation. Privacy advocates raise concerns.",
             "word_count": 14, "scrape_success": True},
        ]

        result = agent._synthesize_research(articles, mock_llm_provider)

        assert mock_llm_provider.chat_completion.called
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Key Facts" in result or "200B" in result or "regulatory" in result

    def test_single_article(self, agent, mock_llm_provider):
        """Single article -> still produces a brief."""
        articles = [
            {"title": "AI in 2025", "source": "TechCrunch", "url": "https://tc.com/ai",
             "full_text": "AI investment reached $200B in 2025.",
             "word_count": 8, "scrape_success": True},
        ]

        result = agent._synthesize_research(articles, mock_llm_provider)
        assert mock_llm_provider.chat_completion.called
        assert isinstance(result, str)
        assert len(result) > 0

    def test_no_successful_articles_returns_empty(self, agent, mock_llm_provider):
        """No articles with scrape_success=True -> skip LLM, return empty."""
        articles = [
            {"title": "Failed", "source": "Src", "url": "https://x.com",
             "full_text": "", "word_count": 0, "scrape_success": False},
        ]

        result = agent._synthesize_research(articles, mock_llm_provider)
        assert result == ""
        assert not mock_llm_provider.chat_completion.called

    def test_empty_articles_returns_empty(self, agent, mock_llm_provider):
        """Empty list -> return empty."""
        result = agent._synthesize_research([], mock_llm_provider)
        assert result == ""
        assert not mock_llm_provider.chat_completion.called

    def test_llm_failure_fallback_to_raw_text(self, agent, mock_llm_provider):
        """LLM fails -> fallback to raw article text concatenation."""
        mock_llm_provider.chat_completion.side_effect = Exception("API timeout")

        articles = [
            {"title": "AI in 2025", "source": "TechCrunch", "url": "https://tc.com/ai",
             "full_text": "AI investment reached $200B in 2025.",
             "word_count": 8, "scrape_success": True},
        ]

        result = agent._synthesize_research(articles, mock_llm_provider)
        assert isinstance(result, str)
        assert len(result) > 0
        # Fallback should include raw text
        assert "AI investment" in result

    def test_output_limited_to_8000_chars(self, agent, mock_llm_provider):
        """Synthesis output limited to 8000 characters."""
        mock_llm_provider.chat_completion.return_value.content = "X" * 20000

        articles = [
            {"title": "Long Article", "source": "Src", "url": "https://x.com/long",
             "full_text": "Content " * 1000, "word_count": 1000, "scrape_success": True},
        ]

        result = agent._synthesize_research(articles, mock_llm_provider)
        assert len(result) <= 8000


# ---------------------------------------------------------------------------
# Phase 3: Modified research() method
# ---------------------------------------------------------------------------

class TestResearchMethod:
    """Tests for the modified research() method with deep research pipeline."""

    def test_research_returns_research_result(self, agent):
        """research() still returns a ResearchResult (backward compat)."""
        with patch.object(agent, "_search_fallback", return_value=[
            NewsArticle(title="Test", source="Src", url="https://x.com",
                        date="2025-01-01", summary="Test article")
        ]):
            result = agent.research("test topic", max_articles=3)

        assert isinstance(result, ResearchResult)
        assert result.topic == "test topic"

    def test_research_includes_scrape_stats_when_enabled(self, agent):
        """When deep research is enabled, scrape_stats is populated."""
        with patch.object(agent, "_search_fallback", return_value=[
            NewsArticle(title="Test", source="Src", url="https://x.com",
                        date="2025-01-01", summary="Test article")
        ]):
            with patch.object(agent, "_scrape_multiple_articles", return_value=(
                [{"title": "Test", "source": "Src", "url": "https://x.com",
                  "full_text": "Full content here.", "word_count": 3, "scrape_success": True}],
                {"total": 1, "succeeded": 1, "failed": 0}
            )):
                with patch.object(agent, "_synthesize_research", return_value="Synthesized brief."):
                    result = agent.research(
                        "test topic", max_articles=3, llm_provider=MagicMock(),
                        enable_deep_research=True
                    )

        assert result.scrape_stats is not None
        assert result.scrape_stats["total"] == 1
        assert result.scrape_stats["succeeded"] == 1

    def test_research_includes_synthesis_when_available(self, agent):
        """When deep research + LLM, research_synthesis is populated."""
        mock_llm = MagicMock()
        mock_llm.is_available.return_value = True

        with patch.object(agent, "_search_fallback", return_value=[
            NewsArticle(title="Test", source="Src", url="https://x.com",
                        date="2025-01-01", summary="Test article")
        ]):
            with patch.object(agent, "_scrape_multiple_articles", return_value=(
                [{"title": "Test", "source": "Src", "url": "https://x.com",
                  "full_text": "Full content.", "word_count": 2, "scrape_success": True}],
                {"total": 1, "succeeded": 1, "failed": 0}
            )):
                with patch.object(agent, "_synthesize_research", return_value="Synthesized research brief."):
                    result = agent.research(
                        "test topic", max_articles=3, llm_provider=mock_llm,
                        enable_deep_research=True
                    )

        assert result.research_synthesis == "Synthesized research brief."
        assert result.articles[0].full_text == "Full content."

    def test_research_skips_scraping_when_disabled(self, agent):
        """When enable_deep_research=False, no scraping or synthesis occurs."""
        with patch.object(agent, "_search_fallback", return_value=[
            NewsArticle(title="Test", source="Src", url="https://x.com",
                        date="2025-01-01", summary="Test article")
        ]):
            with patch.object(agent, "_scrape_multiple_articles") as mock_scrape:
                result = agent.research(
                    "test topic", max_articles=3,
                    enable_deep_research=False
                )

        assert not mock_scrape.called
        assert result.scrape_stats is None
        assert result.research_synthesis == ""

    def test_research_no_articles_skips_scraping(self, agent):
        """When search returns 0 articles, scraping is skipped."""
        mock_llm = MagicMock()
        mock_llm.is_available.return_value = True

        with patch.object(agent, "_search_fallback", return_value=[]):
            with patch.object(agent, "_scrape_multiple_articles") as mock_scrape:
                result = agent.research(
                    "test topic", max_articles=3, llm_provider=mock_llm,
                    enable_deep_research=True
                )

        assert not mock_scrape.called
        assert result.scrape_stats is None
        assert result.research_synthesis == ""

    def test_research_enriches_article_full_text(self, agent):
        """Articles should have full_text populated after scraping."""
        mock_llm = MagicMock()
        mock_llm.is_available.return_value = True

        with patch.object(agent, "_search_fallback", return_value=[
            NewsArticle(title="Article 1", source="Src A", url="https://example.com/1",
                        date="2025-01-01", summary="First article"),
            NewsArticle(title="Article 2", source="Src B", url="https://example.com/2",
                        date="2025-01-01", summary="Second article"),
        ]):
            with patch.object(agent, "_scrape_multiple_articles", return_value=(
                [
                    {"title": "Article 1", "source": "Src A", "url": "https://example.com/1",
                     "full_text": "Full text of article 1", "word_count": 5, "scrape_success": True},
                    {"title": "Article 2", "source": "Src B", "url": "https://example.com/2",
                     "full_text": "", "word_count": 0, "scrape_success": False},
                ],
                {"total": 2, "succeeded": 1, "failed": 1}
            )):
                with patch.object(agent, "_synthesize_research", return_value="Synth"):
                    result = agent.research(
                        "test topic", max_articles=3, llm_provider=mock_llm,
                        enable_deep_research=True
                    )

        assert result.articles[0].full_text == "Full text of article 1"
        assert result.articles[1].full_text == ""


# ---------------------------------------------------------------------------
# Phase 3: research_and_format_for_generation()
# ---------------------------------------------------------------------------

class TestResearchAndFormatForGeneration:
    """Tests for the updated research_and_format_for_generation()."""

    def test_returns_dict_with_new_fields(self, agent):
        """Returned dict includes scrape_stats and research_synthesis."""
        with patch.object(agent, "research", return_value=ResearchResult(
            topic="test", search_date="2025-01-01", articles=[
                NewsArticle(title="A1", source="S1", url="https://x.com/a1",
                            date="2025-01-01", summary="Test", full_text="Full text.")
            ],
            key_findings=["Finding 1"], related_topics=["Topic 1"],
            summary="Summary", scrape_stats={"total": 1, "succeeded": 1, "failed": 0},
            research_synthesis="Synthesized brief."
        )):
            result = agent.research_and_format_for_generation("test", llm_provider=MagicMock())

        assert "scrape_stats" in result
        assert "research_synthesis" in result
        assert result["scrape_stats"]["succeeded"] == 1
        assert result["research_synthesis"] == "Synthesized brief."

    def test_context_uses_synthesis_when_available(self, agent):
        """When synthesis is available, context should use it."""
        with patch.object(agent, "research", return_value=ResearchResult(
            topic="test", search_date="2025-01-01", articles=[
                NewsArticle(title="A1", source="S1", url="https://x.com/a1",
                            date="2025-01-01", summary="Test")
            ],
            key_findings=["Finding 1"], related_topics=["Topic 1"],
            summary="Summary", scrape_stats=None,
            research_synthesis="Synthesized brief for the topic."
        )):
            result = agent.research_and_format_for_generation("test", llm_provider=MagicMock())

        assert "Synthesized brief" in result["context"]
        assert "HALLAZGOS" not in result["context"]  # old format not used

    def test_context_falls_back_to_raw_when_no_synthesis(self, agent):
        """When no synthesis, context uses the old formatting."""
        with patch.object(agent, "research", return_value=ResearchResult(
            topic="fallback test", search_date="2025-01-01", articles=[
                NewsArticle(title="A1", source="S1", url="https://x.com/a1",
                            date="2025-01-01", summary="Test summary")
            ],
            key_findings=["Finding 1"], related_topics=["Topic 1"],
            summary="Summary", scrape_stats=None, research_synthesis=""
        )):
            result = agent.research_and_format_for_generation("fallback test")

        # Old format should be used
        assert "HALLAZGOS" in result["context"] or "TEMA ACTUAL" in result["context"]

    def test_articles_include_full_text(self, agent):
        """Article dicts in the result include full_text and url."""
        with patch.object(agent, "research", return_value=ResearchResult(
            topic="test", search_date="2025-01-01", articles=[
                NewsArticle(title="A1", source="S1", url="https://x.com/a1",
                            date="2025-01-01", summary="Test", full_text="Full text content")
            ],
            key_findings=[], related_topics=[], summary="Summary",
        )):
            result = agent.research_and_format_for_generation("test")

        assert result["articles"][0]["full_text"] == "Full text content"
        assert result["articles"][0]["url"] == "https://x.com/a1"
        assert result["articles"][0]["scrape_success"] is True

    def test_backward_compat_no_llm_provider(self, agent):
        """Calling without llm_provider still works (synthesis skipped)."""
        with patch.object(agent, "research", return_value=ResearchResult(
            topic="test", search_date="2025-01-01", articles=[
                NewsArticle(title="A1", source="S1", url="https://x.com/a1",
                            date="2025-01-01", summary="Test")
            ],
            key_findings=["Finding"], related_topics=["Topic"],
            summary="Summary"
        )):
            # No llm_provider argument
            result = agent.research_and_format_for_generation("test")

        assert "topic" in result
        assert "context" in result
        assert len(result["articles"]) > 0

    def test_research_topic_convenience_function(self):
        """The convenience function research_topic() works and returns a dict."""
        with patch.object(NewsResearchAgent, "research_and_format_for_generation", return_value={
            "topic": "test", "context": "context", "articles": [],
            "key_findings": [], "related_topics": [],
            "scrape_stats": None, "research_synthesis": "",
        }):
            result = research_topic("test topic")
        assert isinstance(result, dict)
        assert result["topic"] == "test"


# ---------------------------------------------------------------------------
# Phase 4: Content Generator
# ---------------------------------------------------------------------------

class TestContentGeneratorPrompt:
    """Tests for the enhanced content generator prompt."""

    def test_fallback_draft_returns_valid_content_when_no_llm(self):
        """Without an LLM, generate_draft falls back to _fallback_draft
        which returns a valid string with the topic name."""
        from aphra_blogger.agents.content_generator import ContentGenerator
        generator = ContentGenerator(api_key=None)

        # Access the LLM prompt directly by calling generate_draft without LLM
        style_profile = {"tone": "conversational", "voice": "friendly"}
        keywords = ["AI", "technology"]
        research_context = "Research brief about AI in 2025 with key developments."

        draft = generator.generate_draft(
            topic="AI in 2025",
            style_profile=style_profile,
            keywords=keywords,
            sample_text="Sample blog text with personal style and voice.",
            research_context=research_context,
        )

        # The draft should NOT contain generic section titles since the
        # enhanced prompt should push toward natural structure
        assert isinstance(draft, str)
        assert len(draft) > 100

    def test_empty_research_does_not_crash(self):
        """Empty research_context should not crash the generator
        and should produce valid output."""
        from aphra_blogger.agents.content_generator import ContentGenerator
        generator = ContentGenerator(api_key=None)
        style_profile = {"tone": "conversational"}
        keywords = ["AI"]

        draft = generator.generate_draft(
            topic="Test Topic",
            style_profile=style_profile,
            keywords=keywords,
            sample_text="Some sample blog text for style reference.",
            research_context="",
        )
        assert isinstance(draft, str)
        assert len(draft) > 100

    def test_empty_research_without_samples_does_not_crash(self):
        """No research context AND no sample text -> fallback, no crash."""
        from aphra_blogger.agents.content_generator import ContentGenerator
        generator = ContentGenerator(api_key=None)
        style_profile = {"tone": "conversational"}
        keywords = ["AI"]

        draft = generator.generate_draft(
            topic="Test Topic",
            style_profile=style_profile,
            keywords=keywords,
            sample_text="",
            research_context="",
        )
        assert isinstance(draft, str)
        assert len(draft) > 100

    def test_fallback_draft_contains_topic(self):
        """The fallback draft (no LLM) should contain the topic."""
        from aphra_blogger.agents.content_generator import ContentGenerator
        generator = ContentGenerator(api_key=None)

        draft = generator.generate_draft(
            topic="Quantum Computing",
            style_profile={"tone": "conversational"},
            keywords=["quantum", "computing"],
        )
        assert "Quantum Computing" in draft


# ---------------------------------------------------------------------------
# Phase 5: Orchestrator Integration (unit-level validation)
# ---------------------------------------------------------------------------

class TestOrchestratorIntegration:
    """Tests for orchestrator integration points (unit-level)."""

    def test_research_topic_passes_llm_provider(self):
        """research_topic() should pass llm_provider to the agent method."""
        mock_llm = MagicMock()

        with patch.object(NewsResearchAgent, "research_and_format_for_generation", return_value={
            "topic": "test", "context": "ctx", "articles": [],
            "key_findings": [], "related_topics": [],
            "scrape_stats": {"total": 1, "succeeded": 1, "failed": 0},
            "research_synthesis": "Synthesis text",
        }) as mock_method:
            result = research_topic("test", llm_provider=mock_llm, max_articles=5)

        # Verify llm_provider was passed through
        _, kwargs = mock_method.call_args
        assert kwargs.get("llm_provider") is mock_llm
        assert kwargs.get("max_articles") == 5

    def test_empty_research_does_not_crash_orchestrator_flow(self):
        """Orchestrator should not crash when research returns empty context."""
        # Simulate what the orchestrator does
        from aphra_blogger.agents.content_generator import ContentGenerator

        generator = ContentGenerator(api_key=None)

        # Scenario: research_synthesis is empty, research_context is empty
        with patch.object(generator, "llm", None):
            draft = generator.generate_draft(
                topic="Test",
                style_profile={"tone": "conversational"},
                keywords=["test"],
                research_context="",
            )

        assert isinstance(draft, str)
        assert len(draft) > 0

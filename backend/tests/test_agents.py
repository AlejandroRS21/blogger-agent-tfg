"""Tests for blogger agents."""

import pytest
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.agents.keyword_extractor import KeywordExtractor
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.critic import CriticAgent
from aphra_blogger.agents.image_selector import ImageSelectorAgent


class TestStyleAnalyzer:
    """Tests for StyleAnalyzer."""
    
    def test_initialization(self):
        """Test agent initialization."""
        analyzer = StyleAnalyzer()
        assert analyzer is not None
    
    def test_analyze_fallback(self):
        """Test fallback analysis when no API key."""
        analyzer = StyleAnalyzer(api_key=None)
        result = analyzer.analyze(["https://javipas.com"])
        
        assert isinstance(result, dict)
        assert 'tone' in result
        assert 'voice' in result
        assert 'expressions' in result
        assert isinstance(result['expressions'], list)
    
    def test_analyze_with_sample_text(self):
        """Test analysis with sample text."""
        analyzer = StyleAnalyzer(api_key=None)
        result = analyzer.analyze(
            ["https://javipas.com"],
            sample_text="Test content"
        )
        
        assert result is not None
        assert 'structure' in result


class TestKeywordExtractor:
    """Tests for KeywordExtractor."""
    
    def test_initialization(self):
        """Test agent initialization."""
        extractor = KeywordExtractor()
        assert extractor is not None
    
    def test_extract_fallback(self):
        """Test fallback extraction."""
        extractor = KeywordExtractor(api_key=None)
        result = extractor.extract(["https://javipas.com"])
        
        assert isinstance(result, dict)
        assert 'keywords' in result
        assert 'expressions' in result
        assert isinstance(result['keywords'], list)
        assert len(result['keywords']) > 0
    
    def test_extract_themes_present(self):
        """Test that themes are extracted."""
        extractor = KeywordExtractor(api_key=None)
        result = extractor.extract(["https://javipas.com"])
        
        assert 'themes' in result
        assert isinstance(result['themes'], list)


class TestContentGenerator:
    """Tests for ContentGenerator."""
    
    def test_initialization(self):
        """Test agent initialization."""
        generator = ContentGenerator()
        assert generator is not None
    
    def test_generate_draft_fallback(self):
        """Test draft generation fallback."""
        generator = ContentGenerator(api_key=None)
        
        style_profile = {
            "tone": "conversational",
            "expressions": ["test", "example"]
        }
        keywords = ["AI", "technology"]
        
        draft = generator.generate_draft(
            topic="Test Topic",
            style_profile=style_profile,
            keywords=keywords
        )
        
        assert isinstance(draft, str)
        assert len(draft) > 100
        assert "Test Topic" in draft
    
    def test_refine_content_fallback(self):
        """Test content refinement fallback."""
        generator = ContentGenerator(api_key=None)
        
        draft = "# Test\n\nContent here."
        critique = {
            "suggestions": ["Improve intro", "Add examples"],
            "coherence_score": 7
        }
        style_profile = {"tone": "casual"}
        
        refined = generator.refine_content(draft, critique, style_profile)
        
        # Should return original if no API
        assert refined == draft


class TestCriticAgent:
    """Tests for CriticAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        critic = CriticAgent()
        assert critic is not None
    
    def test_critique_fallback(self):
        """Test critique fallback."""
        critic = CriticAgent(api_key=None)
        
        content = """# Test Post
        
## Introduction
This is a test post with some content.

## Body
More content here with details.

## Conclusion
Final thoughts."""
        
        style_profile = {
            "tone": "conversational",
            "expressions": ["test"]
        }
        
        result = critic.critique(content, style_profile, "Test Topic")
        
        assert isinstance(result, dict)
        assert 'coherence_score' in result
        assert 'style_match' in result
        assert 'suggestions' in result
        assert 'needs_revision' in result
        assert isinstance(result['suggestions'], list)
    
    def test_critique_scores_range(self):
        """Test that scores are in valid range."""
        critic = CriticAgent(api_key=None)
        
        content = "# Test\n\nSome content here."
        result = critic.critique(content, {}, "Test")
        
        assert 0 <= result['coherence_score'] <= 10
        assert 0 <= result['style_match'] <= 10


class TestImageSelectorAgent:
    """Tests for ImageSelectorAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        selector = ImageSelectorAgent()
        assert selector is not None
    
    def test_select_images_fallback(self):
        """Test image selection fallback."""
        selector = ImageSelectorAgent(api_key=None)
        
        content = """# Test Post

## Section 1
Content

## Section 2
More content"""
        
        result = selector.select_images(content, "Test Topic", num_images=3)
        
        assert isinstance(result, list)
        assert len(result) == 3
        
        # Check first image (header)
        assert result[0]['position'] == 'header'
        assert 'prompt' in result[0]
        assert 'alt_text' in result[0]
    
    def test_image_structure(self):
        """Test that images have required fields."""
        selector = ImageSelectorAgent(api_key=None)
        
        result = selector.select_images("# Test", "Topic", num_images=2)
        
        for image in result:
            assert 'position' in image
            assert 'prompt' in image
            assert 'alt_text' in image
            assert isinstance(image['prompt'], str)
            assert len(image['prompt']) > 10  # Non-empty prompt


class TestAgentIntegration:
    """Integration tests for agents working together."""
    
    def test_full_pipeline_fallback(self):
        """Test complete pipeline with all agents (fallback mode)."""
        # Initialize all agents
        style_analyzer = StyleAnalyzer(api_key=None)
        keyword_extractor = KeywordExtractor(api_key=None)
        content_generator = ContentGenerator(api_key=None)
        critic = CriticAgent(api_key=None)
        image_selector = ImageSelectorAgent(api_key=None)
        
        # Run pipeline
        urls = ["https://javipas.com"]
        topic = "AI in Education"
        
        # Phase 1: Style analysis
        style = style_analyzer.analyze(urls)
        assert style is not None
        
        # Phase 2: Keyword extraction
        keywords_result = keyword_extractor.extract(urls)
        keywords = keywords_result.get('keywords', [])
        assert len(keywords) > 0
        
        # Phase 3: Content generation
        draft = content_generator.generate_draft(topic, style, keywords)
        assert len(draft) > 500
        
        # Phase 4: Critique
        critique = critic.critique(draft, style, topic)
        assert critique['overall_score'] >= 0
        
        # Phase 5: Images
        images = image_selector.select_images(draft, topic)
        assert len(images) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

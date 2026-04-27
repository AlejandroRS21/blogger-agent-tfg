# Agents - Blogger Agent TFG

> AI agents for analyzing and generating blog content in a specific blogger's style

## 📋 Overview

This package contains specialized AI agents that work together to analyze a blogger's writing style and generate new content that mimics their tone, voice, and structure.

## 🤖 Agents

### 1. StyleAnalyzer 🎭
**File:** `style_analyzer.py`  
**Purpose:** Analyzes writing style characteristics

**Capabilities:**
- Tone detection (conversational, formal, humorous)
- Voice identification (first/third person, perspective)
- Structure pattern analysis
- Characteristic expression extraction
- Sentence and paragraph metrics

**Usage:**
```python
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.llm.factory import LLMFactory

provider = LLMFactory.create("huggingface", token="hf_...")
analyzer = StyleAnalyzer(provider=provider)
style = analyzer.analyze(blogger_urls=["https://javipas.com"])
```

**Output Structure:**
```python
{
    "tone": str,
    "voice": str,
    "language_level": str,
    "structure": str,
    "expressions": List[str],
    "avg_sentence_length": int,
    "paragraph_pattern": str,
    "use_of_humor": str,
    "technical_depth": str,
    "personality_traits": List[str],
    "engagement_style": str
}
```

---

### 2. KeywordExtractor 🔑
**File:** `keyword_extractor.py`  
**Purpose:** Extracts keywords and recurring phrases

**Capabilities:**
- Topic keyword extraction
- Characteristic phrase identification
- Technical term detection
- Theme categorization

**Usage:**
```python
from aphra_blogger.agents.keyword_extractor import KeywordExtractor

provider = LLMFactory.create("huggingface", token="hf_...")
extractor = KeywordExtractor(provider=provider)
result = extractor.extract(blogger_urls=["https://javipas.com"])
```

**Output Structure:**
```python
{
    "keywords": List[str],           # 20-30 main keywords
    "expressions": List[str],        # 10-15 characteristic phrases
    "technical_terms": List[str],    # 5-10 technical terms
    "themes": List[str]              # 5-10 major themes
}
```

---

### 3. ContentGenerator 📝
**File:** `content_generator.py`  
**Purpose:** Generates blog content matching the style

**Capabilities:**
- Draft generation from topic
- Style application
- Content refinement based on critique
- Length control (word count)

**Usage:**
```python
from aphra_blogger.agents.content_generator import ContentGenerator

provider = LLMFactory.create("huggingface", token="hf_...")
generator = ContentGenerator(provider=provider)

# Generate draft
draft = generator.generate_draft(
    topic="El futuro de la IA",
    style_profile=style,
    keywords=keywords,
    min_words=1500,
    max_words=2500
)

# Refine based on critique
refined = generator.refine_content(
    draft=draft,
    critique_feedback=critique,
    style_profile=style
)
```

**Parameters:**
- `topic`: Subject to write about
- `style_profile`: From StyleAnalyzer
- `keywords`: From KeywordExtractor
- `min_words`: Minimum word count
- `max_words`: Maximum word count

---

### 4. CriticAgent 🔍
**File:** `critic.py`  
**Purpose:** Reviews and critiques generated content

**Capabilities:**
- Coherence evaluation
- Style matching assessment
- Engagement scoring
- Improvement suggestions
- Revision recommendations

**Usage:**
```python
from aphra_blogger.agents.critic import CriticAgent

provider = LLMFactory.create("huggingface", token="hf_...")
critic = CriticAgent(provider=provider)
critique = critic.critique(
    content=draft,
    style_profile=style,
    topic="Test Topic"
)
```

**Output Structure:**
```python
{
    "coherence_score": int,      # 0-10
    "style_match": int,          # 0-10
    "engagement_score": int,     # 0-10
    "authenticity_score": int,   # 0-10
    "overall_score": float,      # Average
    "strengths": List[str],      # 2-3 strong points
    "weaknesses": List[str],     # 2-3 weak points
    "suggestions": List[str],    # 3-5 improvements
    "needs_revision": bool       # True if score < 7
}
```

---

### 5. ImageSelectorAgent 🖼️
**File:** `image_selector.py`  
**Purpose:** Selects image placements and generates prompts

### 6. HTMLBuilder 🏗️
**File:** `html_builder.py`
**Purpose:** Converts Markdown to HTML/JSX with SEO metadata

**Capabilities:**
- Markdown → HTML conversion (python-markdown)
- JSX generation for React/Next.js components
- Heading extraction for table of contents (TOC)
- Meta tag generation (title, description, keywords)
- Reading time and word count calculation
- Complete Next.js component generation

### 7. ResearchAgent 🔬
**File:** `research_agent.py`
**Purpose:** Topic research and context exploration

**Capabilities:**
- Topic background research
- Context gathering for content generation
- Supplementary information retrieval

**Capabilities:**
- Strategic image placement
- AI image generation prompts
- Alt text for accessibility
- Context-aware suggestions

**Usage:**
```python
from aphra_blogger.agents.image_selector import ImageSelectorAgent

provider = LLMFactory.create("huggingface", token="hf_...")
selector = ImageSelectorAgent(provider=provider)
images = selector.select_images(
    content=final_content,
    topic="AI in Education",
    num_images=3
)
```

**Output Structure:**
```python
[
    {
        "position": str,      # "header", "section-1", etc.
        "prompt": str,        # Detailed generation prompt
        "alt_text": str,      # Accessible description
        "context": str        # Why this image here
    },
    ...
]
```

---

## 🔄 Agent Workflow

Agents work together in a coordinated pipeline:

```
1. StyleAnalyzer
   ↓ (style_profile)
2. KeywordExtractor
   ↓ (keywords, expressions)
3. ContentGenerator.generate_draft()
   ↓ (draft_content)
4. CriticAgent
   ↓ (critique_feedback)
5. ContentGenerator.refine_content()  [if needed]
   ↓ (final_content)
6. ImageSelectorAgent
   ↓ (image_prompts)
→ Complete blog post
```

## 🛡️ Fallback Behavior

All agents implement fallback behavior when LLM APIs are unavailable:

- **StyleAnalyzer**: Returns predefined Javi Pas style profile
- **KeywordExtractor**: Returns known keywords and expressions
- **ContentGenerator**: Template-based generation
- **CriticAgent**: Rule-based heuristic evaluation
- **ImageSelectorAgent**: Position-based default prompts
- **HTMLBuilder**: Local Markdown→HTML conversion without LLM
- **ResearchAgent**: Returns cached/predefined context

This ensures the system works even without API access.

## 🧪 Testing

```bash
# Run all agent tests
pytest tests/test_agents.py -v

# Test specific agent
pytest tests/test_agents.py::TestStyleAnalyzer -v

# Test with coverage
pytest tests/test_agents.py --cov=aphra_blogger.agents
```

## ⚙️ Configuration

### API Keys

Set environment variables:
```bash
# Primary provider (free)
export HF_TOKEN="hf_..."

# Optional fallback providers
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
```

### Model Selection

```python
# Use different providers
from aphra_blogger.llm.factory import LLMFactory

# HuggingFace (free, primary)
provider = LLMFactory.create("huggingface", token=os.environ["HF_TOKEN"])

# OpenAI (paid fallback)
provider = LLMFactory.create("openai", api_key=os.environ["OPENAI_API_KEY"])

# Gemini (Google)
provider = LLMFactory.create("gemini", api_key=os.environ["GEMINI_API_KEY"])
```

## 📊 Example: Complete Pipeline

```python
from aphra_blogger.agents import (
    StyleAnalyzer, KeywordExtractor, ContentGenerator,
    CriticAgent, ImageSelectorAgent
)
from aphra_blogger.llm.factory import LLMFactory

# Initialize LLM provider
provider = LLMFactory.create("huggingface", token="hf_...")

# Initialize all agents
style_analyzer = StyleAnalyzer(provider=provider)
keyword_extractor = KeywordExtractor(provider=provider)
content_generator = ContentGenerator(provider=provider)
critic = CriticAgent(provider=provider)
image_selector = ImageSelectorAgent(provider=provider)

# Run pipeline
urls = ["https://javipas.com"]
topic = "OpenClaw me alucina"

# 1. Analyze style
style = style_analyzer.analyze(urls)

# 2. Extract keywords
keywords_data = keyword_extractor.extract(urls)
keywords = keywords_data['keywords']

# 3. Generate draft
draft = content_generator.generate_draft(topic, style, keywords)

# 4. Critique
critique_result = critic.critique(draft, style, topic)

# 5. Refine (if needed)
if critique_result['needs_revision']:
    final = content_generator.refine_content(draft, critique_result, style)
else:
    final = draft

# 6. Select images
images = image_selector.select_images(final, topic, num_images=3)

# Result
print(f"Generated {len(final.split())} words")
print(f"Overall score: {critique_result['overall_score']}/10")
print(f"Images: {len(images)}")
```

## 🔧 Customization

### Custom Prompts

Each agent can be extended with custom prompts:

```python
class CustomContentGenerator(ContentGenerator):
    def generate_draft(self, topic, style_profile, keywords, **kwargs):
        # Add custom prompt engineering
        return super().generate_draft(topic, style_profile, keywords, **kwargs)
```

### Custom Scoring

```python
class CustomCritic(CriticAgent):
    def _fallback_critique(self, content):
        # Implement custom scoring logic
        score = self._calculate_custom_score(content)
        return {...}
```

### Custom Provider

```python
from aphra_blogger.llm.base import BaseLLMProvider

class CustomProvider(BaseLLMProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        # Custom implementation
        ...
```

## 📝 Best Practices

1. **Always handle missing API keys**: All agents support fallback mode
2. **Use HuggingFace as primary**: Free Inference API with good quality
3. **Cache style profiles**: StyleAnalyzer results can be reused
4. **Batch keyword extraction**: Extract once, use multiple times
5. **Monitor costs**: Only use paid providers (OpenAI, Gemini) as fallback
6. **Test fallbacks**: Ensure system works without any API

## 🚀 Performance Tips

- Use HuggingFace (free) as primary provider for all agents
- Use OpenAI/Gemini only as fallback when HF is unavailable
- Cache StyleAnalyzer results (they don't change often)
- Implement rate limiting for API calls
- Use async calls for parallel agent execution

## 🐛 Troubleshooting

### Error: "HuggingFace token not found"

```bash
export HF_TOKEN="hf_..."
```
Get your free token at: https://huggingface.co/settings/tokens

### Error: "Rate limit exceeded"

Implement exponential backoff or switch to a paid provider (OpenAI/Gemini) as fallback.

### Poor content quality

- Use a larger model via HF (e.g., Llama 3.1 70B instead of 8B)
- Increase `temperature` for more creative content
- Provide more detailed style profiles

## 📚 References

- [HuggingFace Inference API Docs](https://huggingface.co/docs/api-inference)
- [Orchestrator README](../src/orchestrator/README.md)
- [Orchestration Plan](../../docs/ORCHESTRATION_PLAN.md)

---

**Last updated:** 10 Feb 2026  
**Version:** 0.1.0

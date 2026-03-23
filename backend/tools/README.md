# Blog Scraper Tool

> Web scraper for extracting clean blog content from WordPress and similar sites

## 📋 Overview

The `BlogScraper` tool is designed to extract blog posts from websites (specifically optimized for WordPress sites like javipas.com) and save them as structured JSON data for corpus analysis and training.

## 🚀 Quick Start

### Basic Usage

```python
from tools.scraper import scrape_javipas

# Scrape javipas.com (convenience function)
posts = scrape_javipas(
    max_posts=20,
    output_file="javipas_corpus.json"
)

print(f"Scraped {len(posts)} posts")
```

### Advanced Usage

```python
from tools.scraper import BlogScraper

# Initialize scraper
scraper = BlogScraper(
    base_url="https://javipas.com",
    delay=1.5,      # Seconds between requests
    max_posts=30,   # Maximum posts to scrape
    timeout=10      # Request timeout
)

# Automatic discovery and scraping
posts = scraper.scrape_blog(
    start_page=1,
    max_pages=3,
    output_file="corpus.json"
)

# Manual URL scraping
urls = [
    "https://javipas.com/post1",
    "https://javipas.com/post2"
]
posts = scraper.scrape_multiple(urls)
```

### Command Line

```bash
# Run directly
cd backend
python -m tools.scraper

# This will scrape javipas.com and save to javipas_corpus.json
```

## 📦 Installation

The scraper requires additional dependencies:

```bash
pip install requests beautifulsoup4 lxml
```

Or install all backend dependencies:

```bash
pip install -r requirements.txt
```

## 🔧 Features

### Content Extraction
- ✅ Clean blog post content (removes ads, scripts, styles)
- ✅ Post titles
- ✅ Author information
- ✅ Publication dates
- ✅ Tags and categories
- ✅ Automatic word count

### Smart Scraping
- ✅ Automatic post discovery from blog homepage
- ✅ Pagination support
- ✅ Rate limiting (configurable delay)
- ✅ Request timeout handling
- ✅ Duplicate URL removal

### Data Management
- ✅ Structured JSON output
- ✅ Corpus metadata (blog URL, scrape date, statistics)
- ✅ Easy loading of saved corpus

## 📊 Data Format

### BlogPost Structure

```python
@dataclass
class BlogPost:
    url: str                    # Full URL of the post
    title: str                  # Post title
    content: str                # Clean text content
    author: Optional[str]       # Author name
    date: Optional[str]         # Publication date
    tags: List[str]             # Post tags
    categories: List[str]       # Post categories
    word_count: int             # Automatic word count
    scraped_at: str             # ISO timestamp of scraping
```

### Output JSON Format

```json
{
  "blog_url": "https://javipas.com",
  "scraped_at": "2026-02-10T15:30:00",
  "post_count": 20,
  "total_words": 25000,
  "posts": [
    {
      "url": "https://javipas.com/post1",
      "title": "Example Post Title",
      "content": "Full post content here...",
      "author": "Javi Pas",
      "date": "2026-02-01",
      "tags": ["IA", "tecnología"],
      "categories": ["Tech"],
      "word_count": 1500,
      "scraped_at": "2026-02-10T15:30:00"
    }
  ]
}
```

## 🎯 Use Cases

### 1. Build Training Corpus

```python
from tools.scraper import scrape_javipas

# Scrape 30 posts for style analysis
posts = scrape_javipas(max_posts=30, output_file="corpus.json")

# Extract all content for analysis
all_content = "\n\n".join(post.content for post in posts)
```

### 2. Analyze Writing Style

```python
from tools.scraper import BlogScraper

scraper = BlogScraper(base_url="https://javipas.com")
posts = scraper.scrape_blog(max_pages=3)

# Calculate average post length
avg_words = sum(p.word_count for p in posts) / len(posts)
print(f"Average post: {avg_words:.0f} words")

# Most common tags
all_tags = [tag for post in posts for tag in post.tags]
print(f"Most used tags: {set(all_tags)}")
```

### 3. Load Existing Corpus

```python
from tools.scraper import BlogScraper

# Load previously scraped data
posts = BlogScraper.load_corpus("javipas_corpus.json")

# Work with loaded posts
for post in posts:
    print(f"{post.title}: {post.word_count} words")
```

### 4. Custom Blog Scraping

```python
from tools.scraper import BlogScraper

# Scrape a different blog
scraper = BlogScraper(
    base_url="https://anotherblog.com",
    delay=2.0  # Be more conservative
)

posts = scraper.scrape_blog(
    start_page=1,
    max_pages=5,
    output_file="anotherblog_corpus.json"
)
```

## ⚙️ Configuration Options

### Scraper Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | str | Required | Base URL of the blog |
| `delay` | float | 1.0 | Seconds between requests |
| `max_posts` | int | 30 | Maximum posts to scrape |
| `timeout` | int | 10 | Request timeout in seconds |

### Scraping Methods

**`scrape_post(url: str)`**
- Scrapes a single post
- Returns `BlogPost` or `None`

**`scrape_multiple(urls: List[str])`**
- Scrapes list of URLs with rate limiting
- Returns `List[BlogPost]`

**`discover_posts(start_page: int, max_pages: int)`**
- Discovers post URLs from blog homepage
- Returns `List[str]` (URLs)

**`scrape_blog(start_page: int, max_pages: int, output_file: str)`**
- Complete workflow: discover + scrape + save
- Returns `List[BlogPost]`

## 🛡️ Rate Limiting

The scraper includes built-in rate limiting to be respectful to servers:

```python
scraper = BlogScraper(
    base_url="https://javipas.com",
    delay=1.5  # Wait 1.5 seconds between requests
)
```

**Recommendations:**
- Use `delay=1.0` minimum (1 second)
- For aggressive scraping: `delay=0.5`
- For conservative scraping: `delay=2.0`
- Default for javipas.com: `delay=1.5`

## 🧪 Testing

```bash
# Run scraper tests
pytest tests/test_scraper.py -v

# Test specific functionality
pytest tests/test_scraper.py::TestBlogPost -v
pytest tests/test_scraper.py::TestBlogScraper -v

# Run with coverage
pytest tests/test_scraper.py --cov=tools.scraper
```

## 🔍 Supported Blog Platforms

The scraper is optimized for **WordPress** sites but supports common patterns:

### HTML Selectors Supported

**Title:**
- `h1.entry-title`
- `h1.post-title`
- `article h1`

**Content:**
- `div.entry-content`
- `div.post-content`
- `article.post`
- `main article`

**Author:**
- `span.author`
- `a.author`
- `[rel="author"]`

**Date:**
- `time[datetime]`
- `span.entry-date`
- `meta[property="article:published_time"]`

**Tags:**
- `a[rel="tag"]`
- `.tags a`

**Post Links:**
- `article h2 a`
- `h2.entry-title a`
- `a[rel="bookmark"]`

## 🚨 Error Handling

The scraper handles common errors gracefully:

- **Network errors:** Logs error and continues
- **Timeout:** Configurable timeout per request
- **Missing content:** Returns `None` for failed posts
- **Invalid HTML:** BeautifulSoup handles malformed HTML

```python
# Errors are logged but don't stop execution
import logging
logging.basicConfig(level=logging.INFO)

scraper = BlogScraper(base_url="https://javipas.com")
posts = scraper.scrape_blog()

# Some posts may fail, others succeed
print(f"Successfully scraped: {len(posts)} posts")
```

## 📝 Example Output

```bash
$ python -m tools.scraper

INFO:tools.scraper:Initialized scraper for https://javipas.com
INFO:tools.scraper:Starting blog scrape of https://javipas.com
INFO:tools.scraper:Discovering posts on page 1
INFO:tools.scraper:Found 10 posts on page 1
INFO:tools.scraper:Discovering posts on page 2
INFO:tools.scraper:Found 10 posts on page 2
INFO:tools.scraper:Discovered 20 unique post URLs
INFO:tools.scraper:Scraping post: https://javipas.com/post1
INFO:tools.scraper:Successfully scraped: Post Title (1250 words)
...
INFO:tools.scraper:Scraped 18 out of 20 posts
INFO:tools.scraper:Saved 18 posts to javipas_corpus.json

Scraped 18 posts
Total words: 22500
```

## 🔗 Integration with Agents

Use scraped corpus with analysis agents:

```python
from tools.scraper import BlogScraper
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.agents.keyword_extractor import KeywordExtractor

# Scrape corpus
posts = BlogScraper.load_corpus("javipas_corpus.json")

# Get URLs for agents
urls = [post.url for post in posts[:10]]

# Analyze style
analyzer = StyleAnalyzer()
style = analyzer.analyze(urls)

# Extract keywords
extractor = KeywordExtractor()
keywords = extractor.extract(urls)

print(f"Style: {style['tone']}")
print(f"Keywords: {keywords['keywords'][:5]}")
```

## 🐛 Troubleshooting

### ImportError: No module named 'bs4'

```bash
pip install beautifulsoup4
```

### ImportError: No module named 'requests'

```bash
pip install requests
```

### No posts discovered

- Check if blog URL is correct
- Verify blog is accessible
- Try increasing `max_pages`
- Check logs for specific errors

### Content extraction fails

- Blog may use different HTML structure
- Add custom selectors (see source code)
- Some sites require JavaScript (use Selenium/Playwright)

## 📚 References

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

---

**Last updated:** 10 Feb 2026  
**Version:** 1.0.0

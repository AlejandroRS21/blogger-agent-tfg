"""
Web scraper for extracting blog content from javipas.com and similar blogs.

This scraper is designed to:
- Extract clean blog post content
- Handle pagination
- Respect rate limits
- Save corpus data in structured format
"""

import time
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging

# Optional dependencies (will use fallback if not available)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class BlogPost:
    """Represents a scraped blog post."""
    url: str
    title: str
    content: str
    author: Optional[str] = None
    date: Optional[str] = None
    tags: List[str] = None
    categories: List[str] = None
    word_count: int = 0
    scraped_at: str = None
    
    def __post_init__(self):
        """Calculate word count and set scraped timestamp."""
        if self.word_count == 0 and self.content:
            self.word_count = len(self.content.split())
        
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()
        
        if self.tags is None:
            self.tags = []
        
        if self.categories is None:
            self.categories = []


class BlogScraper:
    """
    Scraper for blog websites, specifically optimized for WordPress sites.
    
    Features:
    - Clean content extraction
    - Rate limiting
    - Pagination support
    - Structured data output
    """
    
    def __init__(
        self,
        base_url: str,
        delay: float = 1.0,
        max_posts: int = 30,
        timeout: int = 10
    ):
        """
        Initialize the blog scraper.
        
        Args:
            base_url: Base URL of the blog (e.g., "https://javipas.com")
            delay: Delay between requests in seconds (default: 1.0)
            max_posts: Maximum number of posts to scrape (default: 30)
            timeout: Request timeout in seconds (default: 10)
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        if not BS4_AVAILABLE:
            raise ImportError("beautifulsoup4 is required. Install with: pip install beautifulsoup4")
        
        self.base_url = base_url.rstrip('/')
        self.delay = delay
        self.max_posts = max_posts
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        logger.info(f"Initialized scraper for {self.base_url}")
    
    def scrape_post(self, url: str) -> Optional[BlogPost]:
        """
        Scrape a single blog post.
        
        Args:
            url: Full URL of the blog post
            
        Returns:
            BlogPost object or None if scraping failed
        """
        try:
            logger.info(f"Scraping post: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract content
            content = self._extract_content(soup)
            
            # Extract metadata
            author = self._extract_author(soup)
            date = self._extract_date(soup)
            tags = self._extract_tags(soup)
            categories = self._extract_categories(soup)
            
            if not title or not content:
                logger.warning(f"Could not extract title or content from {url}")
                return None
            
            post = BlogPost(
                url=url,
                title=title,
                content=content,
                author=author,
                date=date,
                tags=tags,
                categories=categories
            )
            
            logger.info(f"Successfully scraped: {title} ({post.word_count} words)")
            return post
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
    
    def scrape_multiple(self, urls: List[str]) -> List[BlogPost]:
        """
        Scrape multiple blog posts with rate limiting.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of successfully scraped BlogPost objects
        """
        posts = []
        
        for i, url in enumerate(urls[:self.max_posts]):
            post = self.scrape_post(url)
            
            if post:
                posts.append(post)
            
            # Rate limiting (except for last request)
            if i < len(urls) - 1:
                time.sleep(self.delay)
        
        logger.info(f"Scraped {len(posts)} out of {len(urls)} posts")
        return posts
    
    def discover_posts(self, start_page: int = 1, max_pages: int = 3) -> List[str]:
        """
        Discover blog post URLs from the main blog page.
        
        Args:
            start_page: Starting page number
            max_pages: Maximum number of pages to crawl
            
        Returns:
            List of discovered post URLs
        """
        urls = []
        
        for page_num in range(start_page, start_page + max_pages):
            logger.info(f"Discovering posts on page {page_num}")
            
            # Common WordPress pagination patterns
            page_url = self._get_page_url(page_num)
            
            try:
                response = self.session.get(page_url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find post links
                post_urls = self._extract_post_links(soup)
                urls.extend(post_urls)
                
                logger.info(f"Found {len(post_urls)} posts on page {page_num}")
                
                # Rate limiting between pages
                if page_num < start_page + max_pages - 1:
                    time.sleep(self.delay)
                    
            except requests.RequestException as e:
                logger.error(f"Error accessing page {page_num}: {e}")
                break
        
        # Remove duplicates while preserving order
        urls = list(dict.fromkeys(urls))
        logger.info(f"Discovered {len(urls)} unique post URLs")
        
        return urls
    
    def scrape_blog(
        self,
        start_page: int = 1,
        max_pages: int = 3,
        output_file: Optional[str] = None
    ) -> List[BlogPost]:
        """
        Complete workflow: discover and scrape posts from blog.
        
        Args:
            start_page: Starting page for discovery
            max_pages: Maximum pages to discover
            output_file: Optional JSON file to save results
            
        Returns:
            List of scraped BlogPost objects
        """
        logger.info(f"Starting blog scrape of {self.base_url}")
        
        # Discover posts
        urls = self.discover_posts(start_page, max_pages)
        
        if not urls:
            logger.warning("No post URLs discovered")
            return []
        
        # Scrape posts
        posts = self.scrape_multiple(urls)
        
        # Save to file if specified
        if output_file and posts:
            self.save_corpus(posts, output_file)
        
        return posts
    
    def save_corpus(self, posts: List[BlogPost], filename: str):
        """
        Save scraped posts to JSON file.
        
        Args:
            posts: List of BlogPost objects
            filename: Output filename
        """
        data = {
            'blog_url': self.base_url,
            'scraped_at': datetime.now().isoformat(),
            'post_count': len(posts),
            'total_words': sum(p.word_count for p in posts),
            'posts': [asdict(post) for post in posts]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(posts)} posts to {filename}")
    
    @staticmethod
    def load_corpus(filename: str) -> List[BlogPost]:
        """
        Load corpus from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            List of BlogPost objects
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        posts = [BlogPost(**post_data) for post_data in data['posts']]
        logger.info(f"Loaded {len(posts)} posts from {filename}")
        
        return posts
    
    # Private helper methods
    
    def _get_page_url(self, page_num: int) -> str:
        """Generate URL for a specific page number."""
        if page_num == 1:
            return self.base_url
        else:
            # Common WordPress pagination
            return f"{self.base_url}/page/{page_num}/"
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract post title from HTML."""
        # Try multiple selectors
        selectors = [
            'h1.entry-title',
            'h1.post-title',
            'article h1',
            'h1',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                # Clean up title (remove site name if present)
                title = re.sub(r'\s*[-|]\s*.*$', '', title)
                return title
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main post content from HTML."""
        # Try multiple selectors for content
        selectors = [
            'div.entry-content',
            'div.post-content',
            'article.post',
            'div.article-content',
            'main article'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Remove scripts, styles, ads
                for tag in element.find_all(['script', 'style', 'iframe', 'aside']):
                    tag.decompose()
                
                # Remove common ad classes
                for ad_class in ['adsbygoogle', 'ad-container', 'advertisement']:
                    for ad in element.find_all(class_=ad_class):
                        ad.decompose()
                
                # Get text content
                content = element.get_text(separator='\n', strip=True)
                
                # Clean up excessive whitespace
                content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
                
                return content.strip()
        
        return None
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract author name."""
        selectors = [
            'span.author',
            'a.author',
            'span.by-author',
            '[rel="author"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return None
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract publication date."""
        selectors = [
            'time[datetime]',
            'span.entry-date',
            'span.post-date',
            'meta[property="article:published_time"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Try to get datetime attribute first
                date = element.get('datetime') or element.get('content')
                if date:
                    return date
                return element.get_text(strip=True)
        
        return None
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract post tags."""
        tags = []
        
        # Try to find tag links
        tag_elements = soup.select('a[rel="tag"]')
        if not tag_elements:
            tag_elements = soup.select('.tags a, .tag-links a')
        
        for tag_elem in tag_elements:
            tag = tag_elem.get_text(strip=True)
            if tag:
                tags.append(tag)
        
        return tags
    
    def _extract_categories(self, soup: BeautifulSoup) -> List[str]:
        """Extract post categories."""
        categories = []
        
        # Try to find category links
        cat_elements = soup.select('a[rel="category tag"]')
        if not cat_elements:
            cat_elements = soup.select('.categories a, .category-links a')
        
        for cat_elem in cat_elements:
            cat = cat_elem.get_text(strip=True)
            if cat:
                categories.append(cat)
        
        return categories
    
    def _extract_post_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract post URLs from a page."""
        urls = []
        
        # Try multiple selectors for post links
        selectors = [
            'article h2 a',
            'article h3 a',
            'h2.entry-title a',
            'h3.entry-title a',
            '.post-title a',
            'article a[rel="bookmark"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for elem in elements:
                    href = elem.get('href')
                    if href:
                        # Make absolute URL
                        full_url = urljoin(self.base_url, href)
                        
                        # Only include URLs from same domain
                        if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                            urls.append(full_url)
                
                # If we found links with this selector, stop trying others
                if urls:
                    break
        
        return urls


# Convenience function for quick scraping
def scrape_javipas(
    max_posts: int = 30,
    output_file: str = "javipas_corpus.json"
) -> List[BlogPost]:
    """
    Convenience function to scrape javipas.com blog.
    
    Args:
        max_posts: Maximum number of posts to scrape
        output_file: Output JSON filename
        
    Returns:
        List of scraped BlogPost objects
    """
    scraper = BlogScraper(
        base_url="https://javipas.com",
        delay=1.5,  # Be respectful
        max_posts=max_posts
    )
    
    posts = scraper.scrape_blog(
        start_page=1,
        max_pages=3,
        output_file=output_file
    )
    
    return posts


if __name__ == '__main__':
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    print("Scraping javipas.com...")
    posts = scrape_javipas(max_posts=20, output_file="javipas_corpus.json")
    
    print(f"\nScraped {len(posts)} posts")
    if posts:
        print(f"Total words: {sum(p.word_count for p in posts)}")
        print(f"\nFirst post: {posts[0].title}")
        print(f"URL: {posts[0].url}")
        print(f"Words: {posts[0].word_count}")

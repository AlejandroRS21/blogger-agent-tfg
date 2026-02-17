"""
Example script demonstrating how to use the BlogScraper.

This script shows:
1. Basic scraping with scrape_javipas()
2. Custom scraper configuration
3. Loading and analyzing corpus
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from tools.scraper import BlogScraper, scrape_javipas
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_1_quick_scrape():
    """Example 1: Quick scraping using convenience function."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Scrape with scrape_javipas()")
    print("="*60)
    
    posts = scrape_javipas(
        max_posts=10,
        output_file="javipas_sample.json"
    )
    
    print(f"\n✅ Scraped {len(posts)} posts")
    print(f"📊 Total words: {sum(p.word_count for p in posts):,}")
    
    if posts:
        print(f"\n📝 First post:")
        print(f"   Title: {posts[0].title}")
        print(f"   URL: {posts[0].url}")
        print(f"   Words: {posts[0].word_count}")
        print(f"   Author: {posts[0].author}")
        print(f"   Tags: {', '.join(posts[0].tags[:3]) if posts[0].tags else 'N/A'}")


def example_2_custom_scraper():
    """Example 2: Custom scraper with manual configuration."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Scraper Configuration")
    print("="*60)
    
    # Create custom scraper
    scraper = BlogScraper(
        base_url="https://javipas.com",
        delay=2.0,  # More conservative
        max_posts=15,
        timeout=15
    )
    
    print(f"🔧 Scraper configured:")
    print(f"   Base URL: {scraper.base_url}")
    print(f"   Delay: {scraper.delay}s")
    print(f"   Max posts: {scraper.max_posts}")
    
    # Discover posts first
    print(f"\n🔍 Discovering posts...")
    urls = scraper.discover_posts(start_page=1, max_pages=2)
    print(f"   Found {len(urls)} post URLs")
    
    if urls:
        print(f"\n   Sample URLs:")
        for url in urls[:3]:
            print(f"   - {url}")
        
        # Scrape discovered posts
        print(f"\n📥 Scraping posts...")
        posts = scraper.scrape_multiple(urls[:5])  # Only first 5
        
        print(f"\n✅ Successfully scraped {len(posts)} posts")
        
        # Save to file
        scraper.save_corpus(posts, "javipas_custom.json")
        print(f"💾 Saved to javipas_custom.json")


def example_3_analyze_corpus():
    """Example 3: Load and analyze existing corpus."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Analyze Existing Corpus")
    print("="*60)
    
    corpus_file = "javipas_sample.json"
    
    if not Path(corpus_file).exists():
        print(f"⚠️  {corpus_file} not found. Run example 1 first.")
        return
    
    print(f"📖 Loading corpus from {corpus_file}...")
    posts = BlogScraper.load_corpus(corpus_file)
    
    print(f"\n📊 Corpus Statistics:")
    print(f"   Total posts: {len(posts)}")
    print(f"   Total words: {sum(p.word_count for p in posts):,}")
    print(f"   Average words per post: {sum(p.word_count for p in posts) / len(posts):.0f}")
    
    # Word count distribution
    word_counts = [p.word_count for p in posts]
    print(f"   Shortest post: {min(word_counts)} words")
    print(f"   Longest post: {max(word_counts)} words")
    
    # Tags analysis
    all_tags = [tag for post in posts for tag in post.tags]
    unique_tags = set(all_tags)
    print(f"\n🏷️  Tags:")
    print(f"   Total tags: {len(all_tags)}")
    print(f"   Unique tags: {len(unique_tags)}")
    if unique_tags:
        print(f"   Sample tags: {', '.join(list(unique_tags)[:5])}")
    
    # Authors
    authors = set(p.author for p in posts if p.author)
    print(f"\n✍️  Authors: {', '.join(authors) if authors else 'N/A'}")
    
    # Show sample content
    print(f"\n📄 Sample Content (first post):")
    if posts:
        content_preview = posts[0].content[:300] + "..." if len(posts[0].content) > 300 else posts[0].content
        print(f"   {content_preview}")


def example_4_single_post():
    """Example 4: Scrape a single specific post."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Scrape Single Post")
    print("="*60)
    
    scraper = BlogScraper(base_url="https://javipas.com")
    
    # You would put a real javipas.com URL here
    # For demonstration, we'll show the concept
    print("📌 To scrape a single post:")
    print("   url = 'https://javipas.com/specific-post-url'")
    print("   post = scraper.scrape_post(url)")
    print("   if post:")
    print("       print(post.title)")
    print("       print(post.content)")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("  BlogScraper Usage Examples")
    print("="*80)
    
    print("\nThis script demonstrates various ways to use the BlogScraper.")
    print("Choose an example to run (or 'all' to run all examples):\n")
    print("  1 - Quick scrape with scrape_javipas()")
    print("  2 - Custom scraper configuration")
    print("  3 - Analyze existing corpus")
    print("  4 - Scrape single post (demo)")
    print("  all - Run all examples")
    print("  q - Quit")
    
    choice = input("\nYour choice: ").strip().lower()
    
    if choice == 'q':
        print("Goodbye!")
        return
    elif choice == '1':
        example_1_quick_scrape()
    elif choice == '2':
        example_2_custom_scraper()
    elif choice == '3':
        example_3_analyze_corpus()
    elif choice == '4':
        example_4_single_post()
    elif choice == 'all':
        example_1_quick_scrape()
        example_2_custom_scraper()
        example_3_analyze_corpus()
        example_4_single_post()
    else:
        print("Invalid choice. Please run again and select 1-4, 'all', or 'q'.")
        return
    
    print("\n" + "="*80)
    print("✅ Examples completed!")
    print("="*80)
    
    print("\n💡 Next steps:")
    print("   - Use scraped corpus with agents:")
    print("     from aphra_blogger.agents.style_analyzer import StyleAnalyzer")
    print("     posts = BlogScraper.load_corpus('javipas_sample.json')")
    print("     analyzer = StyleAnalyzer()")
    print("     style = analyzer.analyze([post.url for post in posts[:5]])")
    print("\n   - Run full orchestrator with real data:")
    print("     python -m src.orchestrator.runner --topic 'Test' --blog-url 'https://javipas.com'")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

"""
Modal deployment for Blogger Agent TFG.

This module deploys the BloggerOrchestrator as a serverless function on Modal.
It provides webhook endpoints for generating blog posts that mimic a blogger's style.

Usage:
    modal deploy backend/modal_app.py
    
Then call the webhook:
    POST https://[your-app]--blogger-agent.modal.run
    {
        "blogger_urls": ["https://javipas.com/post1", "https://javipas.com/post2"],
        "topic": "Las mejores prácticas para desarrollar APIs REST con Python"
    }
"""

import modal
import os
from typing import Dict, Any, List

# Create Modal app
app = modal.App("blogger-agent-tfg")

# Create Docker image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.txt")
    .apt_install("git")  # For potential git operations
)

# Define secrets (will need to be configured in Modal dashboard)
# modal secret create openai-secret OPENAI_API_KEY=sk-...


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("openai-secret")],
    timeout=600,  # 10 minutes max
    memory=2048,  # 2GB RAM
)
def generate_blog_post(
    blogger_urls: List[str],
    topic: str,
    enable_critique: bool = True,
    min_word_count: int = 800,
    max_word_count: int = 2500,
) -> Dict[str, Any]:
    """
    Generate a blog post that mimics the style of the given blogger.
    
    This function orchestrates all agents to:
    1. Analyze the blogger's writing style
    2. Extract keywords and patterns
    3. Generate content with that style
    4. Critique and refine the content
    5. Build HTML/JSX structure
    6. Select image placement prompts
    
    Args:
        blogger_urls: List of URLs from the blogger to analyze
        topic: Topic to write about
        enable_critique: Whether to enable critique phase (default: True)
        min_word_count: Minimum words for generated content (default: 800)
        max_word_count: Maximum words for generated content (default: 2500)
        
    Returns:
        Dict with complete blog post data:
        {
            "workflow_id": "abc123",
            "topic": "...",
            "blogger_urls": [...],
            "style_profile": {...},
            "keywords": [...],
            "content": "...",
            "html_structure": {
                "html": "...",
                "jsx": "...",
                "metadata": {...},
                "headings": [...],
                "nextjs_component": "..."
            },
            "image_prompts": [...],
            "metadata": {
                "duration": 1.5,
                "phases": {...}
            }
        }
    """
    # Import here to avoid loading during image build
    from src.orchestrator.main import BloggerOrchestrator
    from src.orchestrator.config import OrchestratorConfig
    
    # Configure orchestrator
    config = OrchestratorConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        enable_critique=enable_critique,
        min_word_count=min_word_count,
        max_word_count=max_word_count,
        verbose=True,
    )
    
    # Create orchestrator
    orchestrator = BloggerOrchestrator(config=config, verbose=True)
    
    # Run the workflow
    result = orchestrator.run(
        topic=topic,
        blogger_urls=blogger_urls,
        output_path=None,  # Don't save to file in serverless
    )
    
    return result


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("openai-secret")],
)
@modal.web_endpoint(method="POST")
def webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Webhook endpoint for generating blog posts.
    
    This is the main entry point for external requests.
    
    Request body:
    {
        "blogger_urls": ["url1", "url2", ...],
        "topic": "Topic to write about",
        "enable_critique": true,  // optional
        "min_word_count": 800,    // optional
        "max_word_count": 2500    // optional
    }
    
    Response:
    {
        "success": true,
        "data": {
            // Complete blog post data (see generate_blog_post return)
        },
        "error": null
    }
    
    Or on error:
    {
        "success": false,
        "data": null,
        "error": "Error message"
    }
    """
    try:
        # Validate required fields
        if "blogger_urls" not in data:
            return {
                "success": False,
                "data": None,
                "error": "Missing required field: blogger_urls"
            }
        
        if "topic" not in data:
            return {
                "success": False,
                "data": None,
                "error": "Missing required field: topic"
            }
        
        # Extract parameters
        blogger_urls = data["blogger_urls"]
        topic = data["topic"]
        enable_critique = data.get("enable_critique", True)
        min_word_count = data.get("min_word_count", 800)
        max_word_count = data.get("max_word_count", 2500)
        
        # Validate types
        if not isinstance(blogger_urls, list):
            return {
                "success": False,
                "data": None,
                "error": "blogger_urls must be a list"
            }
        
        if not isinstance(topic, str):
            return {
                "success": False,
                "data": None,
                "error": "topic must be a string"
            }
        
        # Call the generator
        result = generate_blog_post.remote(
            blogger_urls=blogger_urls,
            topic=topic,
            enable_critique=enable_critique,
            min_word_count=min_word_count,
            max_word_count=max_word_count,
        )
        
        return {
            "success": True,
            "data": result,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("openai-secret")],
)
def scrape_blogger_corpus(
    blog_url: str,
    max_posts: int = 30,
    delay: float = 1.0,
) -> Dict[str, Any]:
    """
    Scrape a blogger's posts to build a corpus.
    
    This is a helper function for building the initial corpus
    without needing to generate a post.
    
    Args:
        blog_url: Base URL of the blog to scrape
        max_posts: Maximum number of posts to scrape (default: 30)
        delay: Delay between requests in seconds (default: 1.0)
        
    Returns:
        Dict with scraped posts:
        {
            "posts": [...],
            "metadata": {...}
        }
    """
    from tools.scraper import BlogScraper
    
    scraper = BlogScraper(
        base_url=blog_url,
        max_posts=max_posts,
        delay=delay,
    )
    
    posts = scraper.scrape_blog()
    
    return {
        "posts": posts,
        "metadata": {
            "count": len(posts),
            "source": blog_url,
            "max_requested": max_posts,
        }
    }


# Local testing
if __name__ == "__main__":
    """
    Local testing without Modal deployment.
    Run: python backend/modal_app.py
    """
    import sys
    sys.path.insert(0, '.')
    
    from src.orchestrator.main import BloggerOrchestrator
    from src.orchestrator.config import OrchestratorConfig
    
    # Test configuration
    print("=" * 80)
    print("LOCAL TESTING - Modal App")
    print("=" * 80)
    print()
    
    # Set mock API key for testing
    os.environ['OPENAI_API_KEY'] = 'sk-test-mock-key-for-local-testing'
    
    # Test parameters
    blogger_urls = [
        "https://javipas.com/example-1",
        "https://javipas.com/example-2",
    ]
    topic = "Las mejores prácticas para desarrollar APIs REST con Python"
    
    print(f"Topic: {topic}")
    print(f"Blogger URLs: {len(blogger_urls)} URLs")
    print()
    
    # Create config
    config = OrchestratorConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        enable_critique=True,
        min_word_count=800,
        max_word_count=2500,
        verbose=True,
        max_retries=1,  # Reduce for faster testing
    )
    
    # Create orchestrator and run
    orchestrator = BloggerOrchestrator(config=config, verbose=True)
    
    try:
        result = orchestrator.run(
            topic=topic,
            blogger_urls=blogger_urls,
            output_path="local_test_output.json"
        )
        
        print()
        print("=" * 80)
        print("LOCAL TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print(f"Workflow ID: {result.get('workflow_id')}")
        print(f"Content Length: {len(result.get('content', ''))} chars")
        print(f"Keywords: {len(result.get('keywords', []))} extracted")
        
        if result.get('html_structure'):
            html = result['html_structure']
            print(f"HTML Length: {len(html.get('html', ''))} chars")
            print(f"JSX Length: {len(html.get('jsx', ''))} chars")
            print(f"Headings: {len(html.get('headings', []))}")
        
        print()
        print("Output saved to: local_test_output.json")
        
    except Exception as e:
        print()
        print("=" * 80)
        print("LOCAL TEST FAILED!")
        print("=" * 80)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

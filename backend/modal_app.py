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
    .add_local_dir("src", "/src", copy=True)
    .add_local_dir("aphra_blogger", "/aphra_blogger", copy=True)
    .add_local_dir("tools", "/tools", copy=True)
    .apt_install("git")
    .env({"PYTHONPATH": "/"})
)

# Define secrets (will need to be configured in Modal dashboard)
# modal secret create openai-secret OPENAI_API_KEY=sk-...
# modal secret create hf-secret HF_TOKEN=hf_...


@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("blogger-agent-secrets"),
    ],
    timeout=600,  # 10 minutes max
    memory=2048,  # 2GB RAM
)
def generate_blog_post(
    blogger_urls: List[str],
    topic: str,
    enable_critique: bool = True,
    min_word_count: int = 800,
    max_word_count: int = 2500,
    provider: str = "huggingface",
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
        provider: LLM provider to use ("huggingface", "openai", "auto")
        
    Returns:
        Dict with complete blog post data
    """
    # Import here to avoid loading during image build
    from src.orchestrator.main import BloggerOrchestrator
    from src.orchestrator.config import OrchestratorConfig
    
    # Configure orchestrator
    config = OrchestratorConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        huggingface_token=os.environ.get("HF_TOKEN"),
        provider=provider,
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
    secrets=[
        modal.Secret.from_name("blogger-agent-secrets"),
    ],
    timeout=900,
    memory=2048,
)
def run_continuous_publishing(
    blogger_urls: List[str],
    topic_candidates: List[Dict[str, Any]],
    cycles: int = 2,
    interval_seconds: float = 0.0,
    provider: str = "auto",
) -> Dict[str, Any]:
    """Run bounded continuous publishing cycles in Modal."""
    from src.orchestrator.main import BloggerOrchestrator
    from src.orchestrator.config import OrchestratorConfig

    config = OrchestratorConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        huggingface_token=os.environ.get("HF_TOKEN"),
        provider=provider,
        enable_continuous_publishing=True,
        write_canonical_docs=True,
        verbose=True,
    )

    orchestrator = BloggerOrchestrator(config=config, verbose=True)
    return orchestrator.start_continuous_publishing(
        blogger_urls=blogger_urls,
        topic_candidates=topic_candidates,
        cycles=cycles,
        interval_seconds=interval_seconds,
    )


@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("blogger-agent-secrets"),
    ],
)
@modal.fastapi_endpoint(method="POST")
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
        "max_word_count": 2500,   // optional
        "provider": "huggingface" // optional
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
        provider = data.get("provider", "huggingface")
        
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
            provider=provider,
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
    secrets=[
        modal.Secret.from_name("blogger-agent-secrets"),
    ],
)
@modal.fastapi_endpoint(method="POST")
def continuous_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """Webhook endpoint for bounded continuous publishing operations."""
    try:
        blogger_urls = data.get("blogger_urls")
        topic_candidates = data.get("topic_candidates")
        if not isinstance(blogger_urls, list) or not blogger_urls:
            return {"success": False, "data": None, "error": "blogger_urls must be a non-empty list"}
        if not isinstance(topic_candidates, list) or not topic_candidates:
            return {"success": False, "data": None, "error": "topic_candidates must be a non-empty list"}

        result = run_continuous_publishing.remote(
            blogger_urls=blogger_urls,
            topic_candidates=topic_candidates,
            cycles=int(data.get("cycles", 2)),
            interval_seconds=float(data.get("interval_seconds", 0.0)),
            provider=data.get("provider", "auto"),
        )
        return {"success": True, "data": result, "error": None}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "data": None, "error": str(e)}


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("blogger-agent-secrets")],
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

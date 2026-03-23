"""
CLI Runner for Blogger Orchestrator.

Provides command-line interface to execute the blogger agent workflow.

Usage:
    python -m src.orchestrator.runner --topic "Your Topic" --blog-url "https://example.com"
    
Example:
    python -m src.orchestrator.runner \
        --topic "OpenClaw me alucina" \
        --blog-url "https://javipas.com" \
        --output "output.json"
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List

from .main import BloggerOrchestrator
from .config import OrchestratorConfig


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Blogger Agent Orchestrator - Generate blog posts mimicking a blogger's style",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python -m src.orchestrator.runner --topic "AI in Education" --blog-url "https://javipas.com"
  
  # Multiple blog URLs
  python -m src.orchestrator.runner \
      --topic "The Future of AI" \
      --blog-url "https://javipas.com" \
      --blog-url "https://javipas.com/category/tech"
  
  # Save output to file
  python -m src.orchestrator.runner \
      --topic "Claude vs ChatGPT" \
      --blog-url "https://javipas.com" \
      --output "generated_post.json"
  
  # Custom configuration
  python -m src.orchestrator.runner \
      --topic "My Topic" \
      --blog-url "https://example.com" \
      --config "custom_config.toml"
      
  # Quiet mode
  python -m src.orchestrator.runner \
      --topic "My Topic" \
      --blog-url "https://example.com" \
      --quiet
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='Topic to write about (e.g., "OpenClaw me alucina")'
    )
    
    parser.add_argument(
        '--blog-url',
        type=str,
        action='append',
        required=True,
        dest='blog_urls',
        help='URL of the blog to analyze for style (can be specified multiple times)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Output file path for generated content (JSON format)'
    )
    
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        help='Path to configuration TOML file'
    )
    
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Suppress progress messages'
    )
    
    parser.add_argument(
        '--no-critique',
        action='store_true',
        help='Disable critique phase'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum number of retries per phase (default: 3)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Blogger Orchestrator v0.1.0'
    )
    
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate command line arguments."""
    # Validate blog URLs
    for url in args.blog_urls:
        if not url.startswith('http://') and not url.startswith('https://'):
            print(f"Error: Invalid URL: {url}", file=sys.stderr)
            print("URLs must start with http:// or https://", file=sys.stderr)
            sys.exit(1)
    
    # Validate config file if provided
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)
    
    # Validate output path
    if args.output:
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_file():
            print(f"Error: Output path is not a file: {args.output}", file=sys.stderr)
            sys.exit(1)


def load_config(args: argparse.Namespace) -> OrchestratorConfig:
    """Load configuration from file or use defaults."""
    if args.config:
        try:
            config = OrchestratorConfig.from_toml(args.config)
        except Exception as e:
            print(f"Error loading config file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Try default location
        default_config = Path(__file__).parent.parent.parent / "aphra_blogger" / "config" / "default.toml"
        if default_config.exists():
            config = OrchestratorConfig.from_toml(str(default_config))
        else:
            config = OrchestratorConfig.default()
    
    # Override with command line args
    if args.no_critique:
        config.enable_critique = False
    
    config.max_retries = args.max_retries
    config.verbose = not args.quiet
    
    return config


def print_result_summary(result: dict) -> None:
    """Print a summary of the generated content."""
    print("\n" + "=" * 70)
    print("✓ GENERATION COMPLETED")
    print("=" * 70)
    print(f"Topic: {result['topic']}")
    print(f"Workflow ID: {result['workflow_id']}")
    print(f"Duration: {result['metadata']['duration']:.2f}s")
    print(f"\nKeywords: {', '.join(result['keywords'])}")
    print(f"\nContent Preview:")
    print("-" * 70)
    content = result['content']
    preview = content[:300] + "..." if len(content) > 300 else content
    print(preview)
    print("-" * 70)
    
    # Word count
    word_count = len(content.split())
    print(f"\nWord Count: {word_count}")
    print(f"Reading Time: ~{word_count // 200} minutes")
    
    # Images
    if result['image_prompts']:
        print(f"\nImage Prompts: {len(result['image_prompts'])}")
        for i, img in enumerate(result['image_prompts'], 1):
            print(f"  {i}. [{img['position']}] {img['prompt']}")
    
    # Errors/Warnings
    if result['metadata']['errors']:
        print(f"\n⚠ Errors: {len(result['metadata']['errors'])}")
        for error in result['metadata']['errors']:
            print(f"  - {error}")
    
    if result['metadata']['warnings']:
        print(f"\n⚠ Warnings: {len(result['metadata']['warnings'])}")
        for warning in result['metadata']['warnings'][:3]:  # Show first 3
            print(f"  - {warning}")
    
    print("=" * 70)


def main() -> int:
    """Main entry point."""
    # Parse arguments
    args = parse_args()
    validate_args(args)
    
    # Load configuration
    try:
        config = load_config(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Create orchestrator
    try:
        orchestrator = BloggerOrchestrator(
            config=config,
            verbose=not args.quiet
        )
    except Exception as e:
        print(f"Error initializing orchestrator: {e}", file=sys.stderr)
        return 1
    
    # Run workflow
    try:
        result = orchestrator.run(
            topic=args.topic,
            blogger_urls=args.blog_urls,
            output_path=args.output
        )
    except KeyboardInterrupt:
        print("\n\nWorkflow interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nError during workflow execution: {e}", file=sys.stderr)
        if config.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    # Print summary
    if not args.quiet:
        print_result_summary(result)
        
    # Guardar el HTML completo en docs/posts/ y actualizar posts.json
    try:
        from pathlib import Path
        # asumiendo que el runner.py está en backend/src/orchestrator/
        docs_dir = Path(__file__).resolve().parent.parent.parent.parent / "docs"
        posts_dir = docs_dir / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        
        slug = result["html_structure"]["metadata"]["slug"]
        html_page_path = posts_dir / f"{slug}.html"
        with open(html_page_path, "w", encoding="utf-8") as f:
            f.write(result["html_structure"]["full_page"])
            
        if not args.quiet:
            print(f"\\n✓ HTML estático guardado en: {html_page_path}")
            
        # Actualizar posts.json
        posts_json_path = docs_dir / "posts.json"
        posts_data = []
        if posts_json_path.exists():
            try:
                with open(posts_json_path, "r", encoding="utf-8") as f:
                    posts_data = json.load(f)
            except Exception:
                pass
                
        # Crear entrada
        titulo = result["html_structure"]["metadata"]["title"] or result["topic"]
        desc = result["html_structure"]["metadata"]["description"] or result["content"][:150] + "..."
        tags = result["html_structure"]["metadata"]["keywords"] or ["IA"]
        
        new_post_meta = {
            "id": slug,
            "title": titulo,
            "description": desc,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": "Blogger Agent",
            "word_count": result["html_structure"]["metadata"]["word_count"],
            "reading_time": result["html_structure"]["metadata"]["reading_time"],
            "tags": tags
        }
        
        # Reemplazar si ya existe
        posts_data = [p for p in posts_data if p.get("id") != slug]
        posts_data.insert(0, new_post_meta)
        
        with open(posts_json_path, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, indent=2, ensure_ascii=False)
            
        if not args.quiet:
            print(f"✓ Índice {posts_json_path.name} actualizado exitosamente.")
            
    except Exception as e:
        print(f"\\nError actualizando el sitio estático (docs/): {e}", file=sys.stderr)
        
    # Save output if requested
    if args.output:
        try:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            if not args.quiet:
                print(f"\n✓ Output saved to: {output_path.absolute()}")
        except Exception as e:
            print(f"Error saving output: {e}", file=sys.stderr)
            return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

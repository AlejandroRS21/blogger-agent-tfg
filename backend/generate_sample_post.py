"""
Script to generate a sample blog post using the real agents and Modal (if configured).
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig

def main():
    print("=" * 70)
    print(" BLOGGER AGENT - SAMPLE POST GENERATION")
    print("=" * 70)

    # Load configuration
    config = OrchestratorConfig()
    
    # IMPORTANT: Select provider. Change to 'modal' for GPU serverless.
    # If MODAL_TOKEN_ID/SECRET are not set, it will fallback to auto.
    config.provider = "modal" 
    config.verbose = True
    config.enable_critique = True
    
    print(f"Using Provider: {config.provider}")
    print("-" * 70)

    # Initialize orchestrator
    try:
        orchestrator = BloggerOrchestrator(config=config, verbose=True)
    except Exception as e:
        print(f"Error initializing orchestrator: {e}")
        return

    # Define parameters
    topic = "Cómo la IA está transformando el desarrollo de software en 2024"
    blogger_urls = [
        "https://javipas.com/2024/01/ia-desarrollo-software/",
    ]

    print(f"Topic: {topic}")
    print(f"Blogger reference: {blogger_urls[0]}")
    print("Running generation... (this may take a few minutes if using GPUs)")
    
    try:
        # Run workflow
        result = orchestrator.run(
            topic=topic,
            blogger_urls=blogger_urls,
            output_path="generated_post_result.json"
        )
        
        print("\n" + "=" * 70)
        print(" GENERATION COMPLETE!")
        print("=" * 70)
        
        # Show results summary
        print(f"Title: {result.get('final_html_data', {}).get('meta_title', 'N/A')}")
        print(f"Word Count: {result.get('final_html_data', {}).get('word_count', 0)} words")
        print(f"Reading Time: {result.get('final_html_data', {}).get('reading_time', 0)} mins")
        
        if 'output_file' in result:
             print(f"\nFinal result saved to: {result['output_file']}")
             
    except Exception as e:
        print(f"\n Workflow failed: {e}")
        print("Suggest checking your Modal deployment or API keys.")

if __name__ == "__main__":
    main()

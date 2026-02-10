"""
Test script to verify the complete orchestrator pipeline with HTMLBuilder integrated.

This script runs a full workflow test to ensure all 7 phases execute properly:
1. Style Analysis
2. Keyword Extraction  
3. Content Generation
4. Critique
5. Refinement (if needed)
6. HTML Building (NEW - Using HTMLBuilder agent)
7. Image Selection
"""

import sys
import os
import json
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig


def test_full_pipeline():
    """Test the complete orchestrator pipeline."""
    print("=" * 80)
    print("TESTING COMPLETE ORCHESTRATOR PIPELINE WITH HTMLBUILDER")
    print("=" * 80)
    print()
    
    # Set mock API key for testing (agents will use placeholders)
    os.environ['OPENAI_API_KEY'] = 'sk-test-mock-key-for-testing-12345'
    
    # Configure orchestrator (using mock data, no API key needed for testing)
    config = OrchestratorConfig.default()
    config.verbose = True
    config.enable_critique = True  # Enable critique and refinement phases
    config.max_retries = 1  # Reduce retries for faster testing
    
    print("Configuration:")
    print(f"  - Enable Critique: {config.enable_critique}")
    print(f"  - Min Word Count: {config.min_word_count}")
    print(f"  - Max Word Count: {config.max_word_count}")
    print(f"  - Max Retries: {config.max_retries}")
    print()
    
    # Initialize orchestrator
    orchestrator = BloggerOrchestrator(config=config, verbose=True)
    
    # Test parameters
    topic = "Las mejores prácticas para desarrollar APIs REST con Python"
    blogger_urls = [
        "https://javipas.com/ejemplo-1",
        "https://javipas.com/ejemplo-2",
    ]
    
    print("Test Parameters:")
    print(f"  - Topic: {topic}")
    print(f"  - Blogger URLs: {len(blogger_urls)} URLs")
    print()
    
    try:
        # Run the complete workflow
        print("Starting workflow execution...")
        print()
        
        result = orchestrator.run(
            topic=topic,
            blogger_urls=blogger_urls,
            output_path="test_workflow_output.json"
        )
        
        print()
        print("=" * 80)
        print("WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        
        # Verify all expected outputs are present
        print("Verification Results:")
        print()
        
        # Check style profile
        if result.get("style_profile"):
            print("✓ Style Profile: Generated")
            print(f"  - Tone: {result['style_profile'].get('tone', 'N/A')}")
        else:
            print("✗ Style Profile: MISSING")
        
        # Check keywords
        if result.get("keywords"):
            print(f"✓ Keywords: {len(result['keywords'])} keywords extracted")
            print(f"  - Sample: {result['keywords'][:3]}")
        else:
            print("✗ Keywords: MISSING")
        
        # Check content
        if result.get("content"):
            word_count = len(result['content'].split())
            print(f"✓ Content: {word_count} words generated")
            print(f"  - Preview: {result['content'][:100]}...")
        else:
            print("✗ Content: MISSING")
        
        # Check HTML structure (NEW - HTMLBuilder output)
        if result.get("html_structure"):
            html = result['html_structure']
            print("✓ HTML Structure: Generated (HTMLBuilder)")
            
            # Check metadata
            if html.get("metadata"):
                meta = html['metadata']
                print(f"  - Title: {meta.get('title', 'N/A')}")
                print(f"  - Description: {meta.get('description', 'N/A')[:60]}...")
                print(f"  - Keywords: {meta.get('keywords', 'N/A')}")
                print(f"  - Reading Time: {meta.get('reading_time', 'N/A')} min")
                print(f"  - Word Count: {meta.get('word_count', 'N/A')}")
            
            # Check HTML
            if html.get("html"):
                print(f"  - HTML: {len(html['html'])} characters")
                print(f"    Preview: {html['html'][:80]}...")
            
            # Check JSX
            if html.get("jsx"):
                print(f"  - JSX: {len(html['jsx'])} characters")
                print(f"    Preview: {html['jsx'][:80]}...")
            
            # Check headings/TOC
            if html.get("headings"):
                print(f"  - Headings (TOC): {len(html['headings'])} headings")
                for i, heading in enumerate(html['headings'][:3], 1):
                    print(f"    {i}. {heading.get('text', 'N/A')} (Level {heading.get('level', 'N/A')})")
            
            # Check Next.js component
            if html.get("nextjs_component"):
                print(f"  - Next.js Component: {len(html['nextjs_component'])} characters")
        else:
            print("✗ HTML Structure: MISSING (HTMLBuilder failed)")
        
        # Check image prompts
        if result.get("image_prompts"):
            print(f"✓ Image Prompts: {len(result['image_prompts'])} prompts")
            for i, img in enumerate(result['image_prompts'][:2], 1):
                print(f"  {i}. Position: {img.get('position', 'N/A')}")
                print(f"     Prompt: {img.get('prompt', 'N/A')[:50]}...")
        else:
            print("✗ Image Prompts: MISSING")
        
        # Check metadata
        if result.get("metadata"):
            meta = result['metadata']
            print()
            print("Workflow Metadata:")
            print(f"  - Duration: {meta.get('duration', 'N/A'):.2f}s")
            
            # Phase summary
            phases = meta.get('phases', {})
            completed = sum(1 for p in phases.values() if p.get('status') == 'completed')
            total = len(phases)
            print(f"  - Phases: {completed}/{total} completed")
            
            # List phase statuses
            print("  - Phase Details:")
            for name, phase in phases.items():
                status = phase.get('status', 'unknown')
                duration = phase.get('duration', 0)
                agent = phase.get('agent_name', 'N/A')
                print(f"    • {name}: {status} ({agent}, {duration:.2f}s)")
            
            # Errors and warnings
            errors = meta.get('errors', [])
            warnings = meta.get('warnings', [])
            if errors:
                print(f"  - Errors: {len(errors)}")
                for error in errors:
                    print(f"    • {error}")
            if warnings:
                print(f"  - Warnings: {len(warnings)}")
        
        print()
        print("=" * 80)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        # Save detailed result for inspection
        output_file = "test_pipeline_result_detailed.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Detailed results saved to: {output_file}")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("TEST FAILED!")
        print("=" * 80)
        print(f"Error: {str(e)}")
        print()
        
        import traceback
        print("Traceback:")
        traceback.print_exc()
        
        return False


if __name__ == "__main__":
    success = test_full_pipeline()
    sys.exit(0 if success else 1)

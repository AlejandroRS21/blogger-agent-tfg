"""
Batch generation script for 50 AI & Big Data topics using the BloggerOrchestrator
and tenacious exponential backoffs to prevent rate-limiting or cost overruns.
"""
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any

from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    before_sleep_log
)

sys.path.insert(0, str(Path(__file__).parent))

from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')
logger = logging.getLogger("BatchGenerator")

# Paths
INPUT_JSON = Path(__file__).parent / "inputs" / "50_ai_bigdata_topics.json"
BATCH_STATUS_JSON = Path(__file__).parent / "batch_status.json"
OUTPUT_DIR = Path(__file__).parent / "outputs" / "batch_gen"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@retry(
    wait=wait_exponential(multiplier=2, min=4, max=60),
    stop=stop_after_attempt(5),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def generate_single_post(topic: str, output_path: str, reference_urls: list[str]) -> Dict[str, Any]:
    """
    Generate a single post with retries for rate-limiting.
    """
    config = OrchestratorConfig.default()
    config.verbose = False
    
    orchestrator = BloggerOrchestrator(config)
    return orchestrator.run(
        topic=topic,
        blogger_urls=reference_urls,
        output_path=output_path
    )

def main():
    parser = argparse.ArgumentParser(description="Batch generate blog posts.")
    parser.add_argument("--input", type=str, default=str(INPUT_JSON), help="Path to input JSON file containing topics.")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR), help="Path to output directory.")
    parser.add_argument("--urls", type=str, nargs="+", default=[
        "https://javipas.com/ejemplo-post-1",
        "https://javipas.com/ejemplo-post-2",
    ], help="List of reference URLs to mimic and analyze")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    reference_urls = args.urls
    
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        logger.error(f"Input JSON missing: {input_path}")
        return
    with open(input_path, "r") as f:
        topics = json.load(f).get("topics", [])
        
    status = {}
    if BATCH_STATUS_JSON.exists():
        with open(BATCH_STATUS_JSON, "r") as f:
            status = json.load(f)
            
    completed_topics = set([k for k, v in status.items() if v.get("success")])
    
    for i, topic in enumerate(topics):
        if topic in completed_topics:
            logger.info(f"Skipping topic {i+1}/{len(topics)} (already generated): {topic}")
            continue
            
        logger.info(f"Generating topic {i+1}/{len(topics)}: {topic}")
        
        safe_name = "".join(c if c.isalnum() else "_" for c in topic)[:50].lower()
        output_path = output_dir / f"{safe_name}.json"
        
        try:
            result = generate_single_post(topic, str(output_path), reference_urls)
            status[topic] = {
                "success": True,
                "metadata": result.get("metadata", {}),
                "output_file": str(output_path)
            }
        except Exception as e:
            logger.error(f"Failed to generate '{topic}' after retries: {str(e)}")
            status[topic] = {"success": False, "error": str(e)}
            
        with open(BATCH_STATUS_JSON, "w") as f:
            json.dump(status, f, indent=2)

if __name__ == "__main__":
    main()

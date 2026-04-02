import json
import logging
import argparse
from pathlib import Path
from tenacity import retry, wait_exponential, stop_after_attempt
import anthropic

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')
logger = logging.getLogger("StyleJudge")

STYLE_PROFILE_FILE = Path(__file__).parent / "javipas_style_profile.json"

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def evaluate_style(text: str, profile_desc: str) -> dict:
    """Send text to Claude to evaluate mimicry vs rigidity against JaviPas."""
    client = anthropic.Anthropic()
    prompt = f"""
    Evaluate the following blog post text for writing style against this specific author rubric profile:
    {profile_desc}
    
    Does it sound like the author? Does it have a rigid templated structure, or is it organically written?
    
    Text snippet: {text[:2000]}
    
    Please provide your response strictly as valid JSON with keys:
    - mimicry_score (1-10, higher means it aligns perfectly with the rubric)
    - rigidity_score (1-10, where 10 is very rigidly templated and 1 is highly organic)
    - analysis (brief string explaining your reasoning)
    """
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            timeout=30.0,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"mimicry_score": 0, "rigidity_score": 0, "analysis": "Failed to parse JSON"}
    except Exception as e:
        logger.error(f"Error during LLM eval: {e}")
        return {"mimicry_score": 0, "rigidity_score": 0, "analysis": "API Error"}

def process_batch(directory: Path):
    """Judge style consistency across all batch files."""
    
    profile_desc = "No reference profile found."
    if STYLE_PROFILE_FILE.exists():
        with open(STYLE_PROFILE_FILE, "r", encoding="utf-8") as f:
            profile_desc = f.read()

    results = {}
    for filepath in directory.glob("*.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                html_content = data.get("content", "")
                text = html_content if html_content else json.dumps(data)
                
                results[filepath.name] = evaluate_style(text, profile_desc)
        except Exception as e:
            logger.error(f"Error processing file {filepath.name}: {e}")
            continue

    if not results:
        return {}
        
    avg_mimicry = sum(r.get("mimicry_score", 0) for r in results.values()) / len(results)
    avg_rigidity = sum(r.get("rigidity_score", 0) for r in results.values()) / len(results)
    
    return {
        "aggregates": {
            "avg_mimicry": avg_mimicry,
            "avg_rigidity": avg_rigidity,
            "total_analyzed": len(results)
        },
        "details": results
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, help="Directory to analyze", default=str(Path(__file__).parent / "outputs" / "batch_gen"))
    parser.add_argument("--report", type=str, help="Path to report output")
    args = parser.parse_args()
    
    path_to_analyze = Path(args.target)
    
    res = process_batch(path_to_analyze)
    print(json.dumps(res, indent=2))
    
    if args.report:
        with open(args.report, "w") as f:
            json.dump(res, f, indent=2)

import json
import math
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@dataclass
class PostStructureMetrics:
    header_count: int
    paragraph_count: int
    image_count: int
    link_count: int
    avg_words_per_paragraph: float

def analyze_structure(html_content: str) -> PostStructureMetrics:
    """Analyze the HTML structure of a blog post."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = soup.find_all('p')
    images = soup.find_all('img')
    links = soup.find_all('a')
    
    avg_wpp = sum(len(p.get_text().split()) for p in paragraphs) / max(len(paragraphs), 1)
    
    return PostStructureMetrics(
        header_count=len(headers),
        paragraph_count=len(paragraphs),
        image_count=len(images),
        link_count=len(links),
        avg_words_per_paragraph=avg_wpp
    )

def process_batch(directory: Path):
    """Analyze structural consistency across all batch files and yield variance score."""
    results = {}
    for filepath in directory.glob("*.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                html_content = data.get("content", "")
                metrics = analyze_structure(html_content)
                results[filepath.name] = asdict(metrics)
        except Exception as e:
            logger.error(f"Failed parsing file: {filepath} ({e})")
            continue
    
    if not results:
        return {}
    
    N = len(results)
    avg_headers = sum(r["header_count"] for r in results.values()) / N
    avg_paragraphs = sum(r["paragraph_count"] for r in results.values()) / N
    avg_images = sum(r["image_count"] for r in results.values()) / N
    avg_links = sum(r["link_count"] for r in results.values()) / N

    # Calculate standard deviation-based variance
    var_headers = sum((r["header_count"] - avg_headers)**2 for r in results.values()) / N
    var_paragraphs = sum((r["paragraph_count"] - avg_paragraphs)**2 for r in results.values()) / N
    
    std_dev_headers = math.sqrt(var_headers)
    std_dev_paragraphs = math.sqrt(var_paragraphs)
    
    return {
        "aggregates": {
            "avg_headers": avg_headers,
            "avg_paragraphs": avg_paragraphs,
            "avg_images": avg_images,
            "avg_links": avg_links,
            "std_dev_headers": std_dev_headers,
            "std_dev_paragraphs": std_dev_paragraphs,
            "total_analyzed": N
        },
        "details": results
    }

if __name__ == "__main__":
    import argparse
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

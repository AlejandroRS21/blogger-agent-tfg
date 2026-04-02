import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any

from backend.structural_analyzer import process_batch as analyze_structural
from backend.style_judge import process_batch as analyze_style

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')
logger = logging.getLogger("AnalysisReport")

@dataclass
class MimicryEvaluationReport:
    total_posts_analyzed: int
    structural_aggregates: Dict[str, Any]
    style_aggregates: Dict[str, Any]
    itemized_results: Dict[str, Any]

def generate_report(output_dir: Path):
    if not output_dir.exists():
        logger.error(f"Directory {output_dir} does not exist.")
        return
        
    structural_res = analyze_structural(output_dir)
    style_res = analyze_style(output_dir)
    
    report_path = Path(__file__).parent.parent / "docs" / "COHERENCE_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    struct_aggs = structural_res.get("aggregates", {})
    style_aggs = style_res.get("aggregates", {})
    
    # Map to schema
    itemized = {}
    for key in set(list(structural_res.get("details", {}).keys()) + list(style_res.get("details", {}).keys())):
        itemized[key] = {
            "structure": structural_res.get("details", {}).get(key, {}),
            "style": style_res.get("details", {}).get(key, {})
        }
        
    report_data = MimicryEvaluationReport(
        total_posts_analyzed=struct_aggs.get('total_analyzed', 0),
        structural_aggregates=struct_aggs,
        style_aggregates=style_aggs,
        itemized_results=itemized
    )
    
    report = f"""# Analysis Report: Generative Code Mimicry vs Rigidity

## Structural Analysis
- **Post Count Analyzed:** {report_data.total_posts_analyzed}
- **Average Headers per Post:** {report_data.structural_aggregates.get('avg_headers', 0):.2f}
- **Average Paragraphs per Post:** {report_data.structural_aggregates.get('avg_paragraphs', 0):.2f}
- **Header Standard Deviation:** {report_data.structural_aggregates.get('std_dev_headers', 0):.4f}
- **Paragraph Standard Deviation:** {report_data.structural_aggregates.get('std_dev_paragraphs', 0):.4f}

## Style Evaluation (Claude-based)
- **Mimicry Score (0-10):** {report_data.style_aggregates.get('avg_mimicry', 0):.2f}
- **Rigidity Score (0-10):** {report_data.style_aggregates.get('avg_rigidity', 0):.2f}
- *Notes: Higher mimicry is better. Lower rigidity indicates less templated "bot" generation.*

## Conclusion
If rigidity is > 7, the prompt needs rework. If mimicry is < 6, the agent needs better context alignment.
"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    # Also dump the raw JSON mapped format
    json_path = report_path.with_suffix('.json')
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report_data), f, indent=2)
    
    logger.info(f"Report saved to {report_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).parent / "outputs" / "batch_gen"
    generate_report(out_dir)

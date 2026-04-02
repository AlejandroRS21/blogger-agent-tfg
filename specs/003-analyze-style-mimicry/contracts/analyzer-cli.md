# CLI Contract: Batch Generation & Evaluation Scripts

## 1. Batch Generator
```bash
python backend/batch_generate.py --input backend/inputs/50_ai_bigdata_topics.json --output docs/posts/
```

**Input (`50_ai_bigdata_topics.json`) Format**:
```json
{
  "topics": [
    "OpenAI releases autonomous coding agents in 2026",
    "Big Data Lakes fully automated by Quantum optimization",
    "...",
    "Anthropic Claude 4.5 changes the AI landscape forever"
  ]
}
```

## 2. Style Mimicry and Structural Analyzer
```bash
python backend/structural_analyzer.py --target docs/posts/ --report docs/COHERENCE_REPORT.md
```

**Output**: Generates `docs/COHERENCE_REPORT.md` combining structural variance and LLM-as-a-judge styles.

### `MimicryEvaluationReport` Output Schema (JSON internal rep)
```json
{
  "total_posts_analyzed": 50,
  "metrics": {
    "structural_variance_score": 0.85,
    "average_style_mimicry_score": 0.90
  },
  "issues": [
    "Posts all start with an interrogative sentence (rigid formula)",
    "Missing Javipas's typical nested blockquotes for side-notes"
  ]
}
```

# Quickstart: Testing Author Mimicry and Structural Variance

Follow these steps to generate 50 AI / Big Data blog posts and analyze them to determine whether the system is truly mimicking Javier Pastor's ("Javipas") writing stylistic fingerprint, or just relying on rigid article structures.

## Prerequisites
- A working Local Python environment with `pytest`, `openai`/`daggr` access.
- Valid API keys for the generation LLM (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`).

## 1. Batch Generate 50 Posts
The repository contains a predefined list of 50 breaking news topics in the AI and Big Data space.
Run the generator script. This will take several minutes as it queues 50 LLM calls:

```bash
cd backend
python batch_generate.py --input inputs/50_ai_bigdata_topics.json --output ../docs/posts/
```

Verify that 50 `.html` or `.md` files are created inside `docs/posts/`.

## 2. Run the Structural and Stylistic Analyzer
Once generation is complete, run the evaluation script to calculate the variation and mimicry overlap:

```bash
python structural_analyzer.py --target ../docs/posts/ --report ../docs/COHERENCE_REPORT.md
```

## 3. Read the Report
Open `docs/COHERENCE_REPORT.md` (or inspect the JSON if outputting structure alone).
- You want a **High Variance Score** (>0.7), meaning the system varies paragraph lengths, headers, and bullet points naturally across topics.
- You want a **High Mimicry Score** (>0.8), meaning the LLM-as-a-judge found characteristic Javipas tone, phrasing, pacing, and quirks.

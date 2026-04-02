# Data Model: Style Mimicry vs Format Rigidity

## Entities

### `BatchGenerationTask`
Represents the batch execution of multiple post generations.
- `id`: *uuid*
- `topic`: *string* (the AI/Big Data concept)
- `status`: *enum* (pending, running, success, failed)
- `output_path`: *string* (path to generated file in `docs/posts/`)
- `error_message`: *string* (if failed)

### `PostStructureMetrics`
The deterministic structural measurements of a given post.
- `post_id`: *string* (slug or topic ID)
- `heading_count`: *int*
- `paragraph_count`: *int*
- `word_count`: *int*
- `bullet_list_count`: *int*
- `link_count`: *int*

### `MimicryEvaluationReport`
The final LLM-as-a-judge score and the consolidated structural variance metric across the 50 posts.
- `total_posts_analyzed`: *int*
- `structural_variance_score`: *float* (0.0=rigid block, 1.0=highly varied)
- `average_style_mimicry_score`: *float* (0.0 to 1.0)
- `observations`: *list[string]* (The LLM's qualitative notes on quirks, tone, and format repetition)
- `per_post_scores`: *list[dict]* (Mapping of each post to its LLM stylistic score)

# Contract: Static Data Fetching

## Description
Since the frontend heavily relies on static files output by the backend orchestrator directly into `docs/posts.json` and `docs/posts/`, the frontend application enforces an input contract based on those directory structures. 

## Expected Formats

### List Contract: `docs/posts.json`
The index payload that drives the homepage:
```json
{
  "posts": [
    {
      "slug": "apple-intelligence-2026",
      "title": "Apple Intelligence en 2026: Una nueva era de agentes locales",
      "date": "2026-04-03T10:00:00Z",
      "excerpt": "Apple por fin libera el SDK local para agentes de IA en sus procesadores M5."
    }
  ]
}
```

### Full Document Contract: `docs/posts/[slug].json`
The static document for `/posts/[slug]`:
```json
{
  "title": "Apple Intelligence en 2026: Una nueva era de agentes locales",
  "content": "<h1>Headline</h1><p>Paragraph text matching author style...</p>",
  "metadata": {
    "style_score": 0.92,
    "structural_variance": 0.78
  }
}
```

If the backend relies on purely outputting standard `.html` files instead (e.g. `docs/posts/apple-intelligence-2026.html`), the contract assumes the HTML `<body>` content is raw markup, and Next.js must extract metadata either from embedded frontmatter or map the list from a sidecar index file.

# Data Model: Frontend Visual Polish & QA

**Feature Branch:** `005-frontend-visual-polish`  
**Description:** Defines state and prop bindings relevant to visual polish (SEO metadata generation and visual bounds handling), as there is no backend state modification in this branch.

## Metadata Definitions

No new persisted backend entities exist. The change purely focuses on how UI models consume the existing `posts.json` and React properties.

### 1. `Metadata` (Next.js Built-in UI DTO)

Constructed on the fly to render `<head>` values using the Next.js `generateMetadata` lifecycle.

**Source**: `frontend/app/lib/api.ts` -> `getPostBySlug(slug)`

**Fields**:
*   `title` (string): Extracted from `post.title`. Bound to `<title>` and `og:title`.
*   `description` (string): Extracted from `post.excerpt`. Bound to `<meta name="description">` and `og:description`.
*   `openGraph` (object): Generates `{ type: 'article', publishedTime: post.date }`.
*   `twitter` (object): Handles Twitter-card formatting, derived similarly. 

## UI View State

The views themselves are purely functional and statically generated (`output: export`). The focus is on container responsiveness and typography rules rather than complex component state loops. Responsive states (`sm:`, `md:`, `lg:`) are driven entirely by viewport width CSS (Tailwind 4) rather than JavaScript listeners.

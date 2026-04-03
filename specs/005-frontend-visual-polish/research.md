# Phase 0: Research

This document captures architectural investigations and technical validations required before implementation.

## Research Findings

### 1. Metadata and OpenGraph in Next.js 14/15/16 App Router
**Task:** Research how to properly generate `metadata` statically for `page.tsx` and dynamic routes like `[slug]`.
*   **Decision:** Use the built-in `export const metadata: Metadata` or `export async function generateMetadata({ params })` from Next.js server components.
*   **Rationale:** Supported natively by Next.js during static export (`output: 'export'`), effectively generating static HTML `<head>` tags.
*   **Alternatives considered:** Manually inserting tags via a custom `Head` component - rejected as it bypasses built-in optimizations and default OpenGraph merging.

### 2. Handling Long Strings and IFrames visually
**Task:** Identify the best CSS approach using Tailwind 4's typography plugin to prevent layout overflow on mobile breakpoints.
*   **Decision:** Apply `break-words` or Tailwind’s `[word-break:break-word]` alongside `@tailwindcss/typography` (`prose`). Ensure `prose-img:max-w-full`, `prose-img:h-auto` are active. Wrap markdown contents in `<article className="prose max-w-none text-balance ...">`.
*   **Rationale:** The `text-balance` and word breaking directly mitigate layout breakage natively when AI hallucinates long strings or unbroken URLs.

### 3. Favicon configuration
**Task:** Standardize favicon integration.
*   **Decision:** Place `icon.ico`, `icon.svg`, and `apple-icon.png` in the `app/` directory so Next.js automatically bundles and generates the relations. Ensure `favicon.ico` exists at `app/favicon.ico`.
*   **Rationale:** The App Router handles `app/favicon.ico` natively without needing explicit link tags.

## Validation Conclusion
- Next.js static generation supports metadata natively without SSR.
- Tailwind 4 typography natively handles most overflow properties, but `text-break` utilities are needed for unbreakable AI artifacts.

# Quickstart: Frontend Visual Polish & QA

**Feature Branch**: `005-frontend-visual-polish`  

This guide provides steps to manually verify the visual fixes and SEO metadata locally.

## 1. Running the Next.js preview

Navigate to the frontend folder and spin up the development server. In dev mode, Next.js will generate elements on the fly simulating static export.

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` in your browser.

## 2. Validating P1 constraints (Responsive Typography)

1. Use Chrome/Firefox Developer Tools (F12) and toggle Device Mode (Ctrl+Shift+M).
2. Set the resolution to typical mobile breakpoints (e.g. 375px width, 414px width).
3. Scroll through `[slug]` pages containing tables or code blocks and ensure text breaks seamlessly without horizontal scrolling (`max-w-prose break-words` should be active).

## 3. Validating P2 constraints (SEO Metadata & OG)

1. Navigate to `/` (Home) and verify the `<title>` tag is dynamically populated using DevTools Elements panel. Ensure `<meta name="description">` exists.
2. Navigate to an article (e.g., `/posts/el-futuro-de-la-ia-en-2026`).
3. Check the DOM `<head>` to ensure `og:title`, `og:description`, and `twitter:card` populate correctly from the localized `getPostBySlug()` mapping.

# Tasks: Frontend Visual Polish & QA

**Feature**: Frontend Visual Polish & QA  
**Branch**: `005-frontend-visual-polish`  
**Goal**: Guarantee 100% responsiveness and correct SEO metadata across all blog pages.

## Status Summary

- **Phase 1: Setup**: 0%
- **Phase 2: Foundational (CSS & Data)**: 0%
- **Phase 3: Responsive Visual Layout (US1)**: 0%
- **Phase 4: Standard Blog Meta-features (US2)**: 0%
- **Phase 5: Polish & QA**: 0%

## Implementation Strategy

We will follow an incremental approach: first fixing the data-mapping issues (slugs) and foundational CSS, then applying mobile-first responsiveness to the post pages, and finally implementing the Next.js Metadata API for SEO.

## Tasks

### Phase 1: Setup
- [x] T001 Commit currently modified files in `frontend/` to stabilize the branch before new changes
- [ ] T002 Verify `docs/posts.json` and `docs/posts/*.json` integrity to ensure every post has a valid `id` or `slug`

### Phase 2: Foundational
- [ ] T003 Fix `generateStaticParams` in `frontend/app/posts/[slug]/page.tsx` to handle potential `undefined` slugs from the data layer
- [ ] T004 [P] Configure global typography rules in `frontend/app/globals.css` ensuring `break-words` and `overflow-wrap` are default for `.prose`
- [ ] T005 [P] Update `frontend/app/lib/api.ts` to strictly sanitize and normalize post object access (ensure fallback for `excerpt` and `slug`)
- [ ] T016 [P] **Implement Zod schema for post data validation to fail-fast during build and prevent "slug undefined" errors**

### Phase 3: Responsive Visual Layout (Story 1)
- [ ] T006 [P] [US1] Update `frontend/app/components/HTMLRenderer.tsx` and `frontend/app/posts/[slug]/page.tsx` to use **responsive prose width and apply text-balance strictly to headings**
- [ ] T007 [P] [US1] Apply responsive grid/flex fixes to `frontend/app/page.tsx` for mobile list view
- [ ] T008 [US1] Implement adaptive sizing for images and code blocks in `.prose` within `frontend/app/globals.css`

### Phase 4: Standard Blog Meta-features (Story 2)
- [ ] T009 [P] [US2] Implement root `metadata` object in `frontend/app/layout.tsx` (site title, site description, favicon refs)
- [ ] T010 [US2] Implement dynamic `generateMetadata` in `frontend/app/posts/[slug]/page.tsx` using `getPostBySlug` data
- [ ] T011 [P] [US2] Add Apple touch icons and favicon link manifests to `frontend/app/layout.tsx`

### Phase 5: Polish & QA
- [ ] T012 Run `npm run build` in `frontend/` to verify static export integrity without errors
- [ ] T013 Manually verify mobile layout (320px) in browser for three different post samples
- [ ] T014 Verify SEO tags presence in `frontend/out/posts/*.html` files after build
- [ ] T015 **Audit all internal links/codes and remove any references to non-static /api routes or legacy components**

## Dependencies

1. **Foundational (T003-T005, T016)** must be completed before **User Story 1 (T006)** to prevent build crashes.
2. **Metadata API (T010)** depends on **API Normalization (T005)**.
3. **QA (T012)** requires all previous phases to be completed.

## Parallel Execution

- T004, T005, T009 can be started in parallel.
- T006, T007 can be started in parallel after T003.

## Test Criteria (US1 & US2)

**User Story 1 - Test Criteria**:
- No horizontal scrollbar on mobile width (320px).
- Post content fills the viewport correctly with readable padding.

**User Story 2 - Test Criteria**:
- Page `<title>` updates correctly per post.
- `<meta name="description">` contains the post excerpt.
- OpenGraph tags (`og:title`, `og:type`) are visible in the build output.

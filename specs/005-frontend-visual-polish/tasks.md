# Tasks: Frontend Visual Polish & Structural Diversity (RE-VERIFIED)

**Feature**: Frontend Visual Polish & Structural Diversity
**Branch**: `005-frontend-visual-polish`
**Goal**: Guarantee 100% responsiveness, correct SEO metadata, and eliminate repetitive structures in AI-generated posts.

## Status Summary

- **Phase 1: Setup**: 100%
- **Phase 2: Foundational (Stability & Data)**: 100%
- **Phase 3: Structural Diversity (Story 1 - Agent Refactor)**: 100%
- **Phase 4: Visual Polish & SEO (Story 2 - UI Experience)**: 100%
- **Phase 5: Polish & QA**: 100%

## Implementation Strategy

We have followed an incremental approach: first securing the data layer with Zod to prevent build crashes, then refactoring the Python agents to support non-rigid structures (Anti-template), and finally applying the visual and SEO polish to the Next.js frontend. All tasks have been verified in a 5-layer audit.

## Tasks

### Phase 1: Setup (Project Initialization)
- [x] T001 Commit currently modified files in `frontend/` to stabilize the branch before new changes
- [x] T002 [P] Verify `docs/posts.json` and `docs/posts/*.json` integrity to ensure every post has a valid `id` or `slug`
- [x] T003 Research and document 3-5 distinct "opening hook" styles from the target corpus `javipas_corpus.json` in `specs/005-frontend-visual-polish/research_hooks.md`

### Phase 2: Foundational (Blocking Prerequisites)
- [x] T004 [P] Implement Zod schema in `frontend/app/types/post.ts` for post data validation to fail-fast during build
- [x] T005 [P] Update `frontend/app/lib/api.ts` to strictly sanitize and normalize post object access (ensure fallback for `excerpt` and `slug`)
- [x] T006 [P] Configure global typography rules in `frontend/app/globals.css` ensuring `break-words` and `overflow-wrap` are default for `.prose`
- [x] T007 Fix `generateStaticParams` in `frontend/app/posts/[slug]/page.tsx` using the new Zod-validated data fetcher

### Phase 3: Structural Diversity (User Story 2 - Python Refactor)
- [x] T008 [US2] Refactor `backend/aphra_blogger/agents/content_generator.py` to replace hardcoded structure with dynamic `structural_mode` prompt logic
- [x] T009 [US2] Update `backend/aphra_blogger/agents/content_generator.py` with 3-5 distinct "opening hook" instructions based on Phase 1 research
- [x] T010 [US2] Create a `pytest` script `backend/tests/test_structural_diversity.py` to verify the generator doesn't produce identical layouts for different runs
- [x] T011 [P] [US2] Update `backend/javipas_prompt_context.txt` with examples of non-rigid article entries (Opinion vs Deep-Dive)

### Phase 4: Visual Polish & SEO (User Story 1 - Frontend Polish)
- [x] T012 [P] [US2] Update `frontend/app/components/HTMLRenderer.tsx` to use responsive prose width and apply `text-balance` strictly to headings
- [x] T013 [P] [US2] Apply adaptive vertical padding and image/code block sizing in `frontend/app/globals.css`
- [x] T014 [US2] Implement dynamic `generateMetadata` in `frontend/app/posts/[slug]/page.tsx` using the validated post data
- [x] T015 [P] [US2] Add standard SEO tags (OG tags, favicon refs, Apple touch icons) to `frontend/app/layout.tsx`

### Phase 5: Polish & QA
- [x] T016 Run `npm run build` in `frontend/` to verify static export integrity and SEO tag presence in `/out`
- [x] T017 Audit all internal links/codes and remove any references to non-static /api routes or legacy components (BlogLayout, PostHeader, etc.)
- [x] T018 Manually verify mobile layout (320px) in browser for three different structural modes (Technical vs Reflective) and document in `specs/005-frontend-visual-polish/mobile-verification.md`

### Phase 6: Critique Remediation (Security & Stability)
- [ ] T019 [P] Implement Iframe Security Sandbox and Whitelist in `frontend/app/components/HTMLRenderer.tsx`
- [ ] T020 [US2] Add HTML Tag Balance check to `backend/aphra_blogger/agents/html_builder.py` to prevent broken layouts
- [ ] T021 Apply `contain: layout` and `content-visibility: auto` to `.prose` in `frontend/app/globals.css` for enhanced performance on long posts
- [ ] T022 [P] Create automated "Post Integrity" audit script (Playwright or node script) to replace manual T018 in future builds

## Dependencies

1. **Foundational (T004-T007)** was completed before **User Story 1 (T008)** to ensure valid data handling during development.
2. **Structural Diversity (T008-T010)** was verified before generating new samples for **UI Testing (Phase 4)**.
3. **Build Integrity (T016)** confirmed all previous tasks work in concert.

## Parallel Execution Examples

- **Data Consistency**: T004 (Zod), T005 (API), T011 (Context) were done in parallel.
- **Visuals**: T012 (HTMLRenderer) and T013 (CSS Padding) were done in parallel.

## MVP Scope Summary
The priority requirement of "Anti-template" generation (User Story 1) has been fully met by introducing `structural_modes` and `opening_hooks` in the Python backend, while the frontend (User Story 2) now provides a visually polished, SEO-ready static site.

---

## Tech Debt Tasks (Generated by /speckit.cleanup)

**Generated**: 2026-04-04
**Source**: Post-implementation cleanup of 005-frontend-visual-polish
**Priority**: Address before next feature iteration

### Detected Issues

- [ ] TD019 [P] Improve error handling granularity in `content_generator.py` during content refinement phase
- [ ] TD020 Implement unified logging system across all agents to replace residual `print()` calls in non-fallback paths

---
description: "Task list for Frontend Web Application & Cloud Deployment"
---

# Tasks: Frontend Web Application & Cloud Deployment

**Input**: Design documents from `specs/004-next-vercel-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/data-fetching-contract.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Next.js scaffold and dependencies required for secure static rendering.

- [x] T001 Update `frontend/package.json` to include an HTML sanitizer like `isomorphic-dompurify` to prevent XSS from AI-generated raw HTML logic (addressing Critique E1).
- [X] T002 [P] Update `frontend/tailwind.config.ts` (or CSS equivalent) to extend the typography and color palette mimicking the target target's blog style profile defined in `backend/javipas_style_profile.json`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Produce internal data fetch wrappers mimicking a generic content API mapped to static JSON structures.

- [x] T003 Create data interface definitions in `frontend/app/types/post.ts` matching the outputs specified in `contracts/data-fetching-contract.md`.
- [x] T004 Create `frontend/app/lib/api.ts` exposing `getAllPosts()` resolving to the root `docs/posts.json` via native Node.js `fs` handling missing file gracefully (addressing Critique E1/E2).
- [x] T005 [P] Create `frontend/app/lib/api.ts` function `getPostBySlug(slug)` addressing the resolution of HTML or Markdown metadata attributes directly from the `docs/posts/` structures.
- [x] T006 Build `frontend/app/components/HTMLRenderer.tsx` leveraging `isomorphic-dompurify` and Tailwind's `@tailwindcss/typography` (`prose`) classes to securely render arbitrary valid HTML.

**Checkpoint**: We have safely established the interface between our Node/Next environment and the raw AI files, while securing the output layer.

---

## Phase 3: User Story 1 - View Blog Homepage (Priority: P1)

**Goal**: Present an infinite scrolling or properly listed responsive homepage parsing JSON files.

**Independent Test**: Load the root browser port and verify a functional UI reading the valid `docs/posts` payload.

### Implementation for User Story 1

- [ ] T007 [US1] Create a functional component `frontend/app/components/PostCard.tsx` strictly rendering basic post information (title, excerpt, date string) leveraging the defined TS interfaces.
- [x] T008 [US1] Update the Server Component `frontend/app/page.tsx` to invoke `getAllPosts()` and render a mapped list using `PostCard`.
- [x] T009 [P] [US1] Enhance the root layout at `frontend/app/layout.tsx` to include a proper standard navigation bar, generic footer mapping the target blog's visual styling.

**Checkpoint**: The homepage now populates locally when static files exist.

---

## Phase 4: User Story 2 - Read Individual Blog Post (Priority: P1)

**Goal**: Full SSG routing matching URLs exactly to the `[slug]` from the data source, faithfully applying structural styling to Markdown/HTML.

**Independent Test**: Route `/posts/apple-intelligence-2026` successfully decodes the mock post into a visually exact HTML representation without raw tag leaks.

### Implementation for User Story 2

- [x] T010 [P] [US2] Implement the Next.js `generateStaticParams` feature inside `frontend/app/posts/[slug]/page.tsx` parsing the full directory list of `docs/posts` to inform SSG path limits.
- [x] T011 [US2] Invoke `getPostBySlug` within `frontend/app/posts/[slug]/page.tsx` utilizing the URL parameter slug to resolve the target document data and catch missing posts with Next.js' `notFound()`.
- [x] T012 [P] [US2] Create a specific metadata summary block `frontend/app/components/PostMeta.tsx` to cleanly inject technical generation statistics beneath or beside the content.
- [x] T013 [US2] Apply `HTMLRenderer` onto the page container and surround it with spacing container constraints to support Edge Case responsive layouts.
- [x] T014 [P] [US2] Add resilient global CSS rules in `frontend/app/globals.css` enforcing max-widths on `<img>` or `<iframe>` tags to avoid layout breaks from LLM hallucinated graphics.

**Checkpoint**: You can fully browse across individual statically generated posts.

---

## Phase 5: User Story 3 - Automate Cloud Deployment (Priority: P2)

**Goal**: The Next.js repository commits reliably yield a live Vercel endpoint reading the exact `docs/` filesystem via SSG logic.

**Independent Test**: Pushing a dummy static file to GitHub correctly propagates the build to the Vercel domain immediately.

### Implementation for User Story 3

- [x] T015 [P] [US3] Create or configure `vercel.json` if necessary to explicitly define build sequences or static path constraints reading the root directory.
- [x] T016 [US3] Finalize `frontend/next.config.mjs` verifying that image domain configurations or static routing rules won't fail out during Vercel's node compilation step due to missing environment keys.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and hardening post-implementation.

- [x] T017 Verify all local Next.js terminal commands (`npm run build`, `npm run start`) function properly when `docs/posts` is completely absent, outputting a friendly "No posts available" Empty State UI.
- [x] T018 Audit all client components strictly looking for hydration errors between Server and Client states explicitly introduced by our `isomorphic-dompurify`.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup & Foundational (Phases 1-2)**: Prerequisite for all routing logic given to the risk of XSS execution logic.
- **User Story 1 & 2 (Phases 3-4)**: Must run concurrently in standard React App routing implementations.
- **User Story 3 (Phase 5)**: Requires the frontend routing layers to complete SSG setup flawlessly before triggering a push to Vercel continuous builds.

### Parallel Opportunities
- Mock layouts (`PostCard.tsx`, `PostMeta.tsx`) and standard HTML render logic (`HTMLRenderer.tsx`) can be coded and styled using static dummy data directly on the files before `api.ts` file system logic is perfectly functional. 
- Vercel JSON setup relies strictly on configuration and can happen in parallel to TS development.

---

## Parallel Example: User Story 1

```bash
# Developers can build components while API endpoints are flushed
Task: T004 Build API mapping (Developer A)
Task: T007 [P] [US1] Build PostCard template (Developer B)
Task: T009 [P] [US1] Build site layout navigation (Developer C)
```

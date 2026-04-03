# Implementation Plan: Frontend Web Application & Cloud Deployment

**Branch**: `004-next-vercel-frontend` | **Date**: 3 de abril de 2026 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-next-vercel-frontend/spec.md`

## Summary

Implement a read-only Next.js web application functioning as a public-facing blog, using Tailwind CSS to mimic a specific author's target style, populated from backend-generated static files inside `docs/posts/`, and automatically deployed via Vercel using Static Site Generation (SSG).

## Technical Context

**Language/Version**: TypeScript 5, Node.js, Next.js 16.1.6, React 19.2.3  
**Primary Dependencies**: Next.js, React, Tailwind CSS 4  
**Storage**: Static JSON and `.html`/`.md` files located in `docs/`  
**Testing**: Jest, React Testing Library  
**Target Platform**: Vercel (Edge/Serverless Platform)
**Project Type**: Web Application (SSG)  
**Performance Goals**: Lighthouse Core Web Vitals >= 90  
**Constraints**: Continuous deployment must complete in <3 minutes; mobile-first responsive design  
**Scale/Scope**: Displaying ~50 AI-generated posts statically

## Constitution Check

*GATE: Passed. Implementation seamlessly adheres to Principal V (Static Delivery as the Canonical Publish Target) by sourcing content strictly from `docs/` and Principle I by keeping the backend uncoupled from the frontend view layer.*

## Project Structure

### Documentation (this feature)

```text
specs/004-next-vercel-frontend/
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Static file TS entities
├── quickstart.md        # Dev/Deployment runbook
├── contracts/           # Integration format boundaries
└── tasks.md             # Implementation steps (future Phase)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── api/             # Vercel Serverless functions (if needed)
│   ├── components/      # React functional components
│   ├── posts/[slug]/    # Dynamic SSG article routes
│   ├── types/           # TS Interfaces driven by contracts
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Homepage index
├── public/              # Static assets
├── tailwind.config.ts   # Style mimicry rules
└── next.config.mjs      # Build config
vercel.json              # Optional Vercel deployment overrides
```

**Structure Decision**: Separating the frontend architecture cleanly under a new `frontend/` directory (or leveraging the existing Next.js App Router scaffold identified in `FRONTEND_IMPLEMENTATION.md`), utilizing Next.js specific paradigms (`app` router) entirely isolated from the Python backend logic.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *N/A* | *N/A* |

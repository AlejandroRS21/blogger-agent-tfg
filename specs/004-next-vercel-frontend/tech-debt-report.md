# Tech Debt Report: Frontend Web Application & Cloud Deployment

**Generated**: 2026-04-03
**Feature**: 004-next-vercel-frontend
**Spec Reference**: [spec.md](./spec.md)

## Executive Summary

| Severity | Count | Immediate Action Required |
|----------|-------|---------------------------|
| Critical | 0 | None |
| Large | 1 | Review and prioritize |
| Medium | 1 | Tasks created in tasks.md |
| Small | 4 | Fixed during cleanup |

## Large Issues Requiring Analysis

### [ISSUE-001] Interactive prototype code violates Constitution

**Category**: Architecture
**Location**: `frontend/app/api/generate-post/route.ts` and `frontend/app/generate/page.tsx`
**Related Spec**: FR-006 (Strict read-only nature of the frontend UI)
**Constitution Impact**: Principle I (Python Pipeline Ownership) & Principle V (Static Delivery)

#### Problem Description

The frontend directory contains pre-existing Next.js App Router code (`generate-post/route.ts` and `generate/page.tsx`) that implements a functional backend call to `localhost:8000` to generate posts interactively from the web UI. 

This violates the newly ratified project constitution:
1. **Principle I** explicitly states that **"All runtime generation... MUST be implemented in Python modules under the backend tree."**
2. **Principle V** asserts that **"Static Delivery [via docs/] is the Canonical Publish Target."** 
3. **Spec FR-006** clarifies that the Next.js app must be "strictly read-only" loading static JSON.

Having an interactive generator UI coupled with the static site generator frontend violates decoupling constraints, creating technical debt that breaks SSG static guarantees if pushed to Vercel (where Vercel Serverless Functions would try calling a localhost backend).

#### Impact if Not Addressed

- Architectural drift: the frontend becomes a monolithic orchestrator rather than a pure presentation layer.
- Vercel Deployment failures: The serverless endpoint expects `BACKEND_URL` config, which isn't part of the SSG build spec.
- Security risk: exposing generation endpoints publicly without auth.

#### Options

**Option 1: Remove Interactive Frontend Code (Recommended)**
- **Approach**: Delete `frontend/app/api/` and `frontend/app/generate/`. Enforce generation strictly through the command line or Gradio instances defined in the backend.
- **Pros**: Perfectly aligns with the Constitution. Secures the Next.js delivery completely as SSG output via `next export`. Reduces bundle size.
- **Cons**: Product owners lose the Next.js web form for triggering generations (if they liked it).
- **Effort**: S
- **Risk**: Low

**Option 2: Feature-Flag & Ignore**
- **Approach**: Ignore the routes in the `next.config.mjs` SSG export by explicitly excluding them from the build.
- **Pros**: Keeps the code around for reference.
- **Cons**: Still violates Principle I in spirit, creates dead code.
- **Effort**: S
- **Risk**: Low

**Option 3: Defer**
- **Approach**: Document and revisit later.
- **Pros**: No immediate effort.
- **Cons**: Risk of the code accidentally leaking or breaking standard Vercel SSG deployment commands.
- **Recommended deferral period**: Never defer a constitution violation.

#### Recommendation

**Option 1 is highly recommended**. The constitution mandates the removal of this architecture. Product owners should rely on `daggr_blogger_workflow.py` or a dedicated Python-backed Gradio instance (if required) for generation orchestration.

---

## Cross-References

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Tasks**: [tasks.md](./tasks.md) (Tech Debt section)
- **Constitution**: [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)

## Next Steps

1. Review this report with stakeholders
2. Decide on approach for each large issue
3. Create implementation tasks for approved remediations
4. Run `/speckit.implement` to address TD tasks

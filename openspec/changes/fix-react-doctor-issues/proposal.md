# Proposal: Fix React Doctor Issues

## Problem
`react-doctor` identified 115 issues in the frontend.

## Scope
- Fix hydration mismatch in `app/page.tsx`.
- Optimize Tailwind palette and icon sizes.
- Add metadata to pages.
- Refactor `NewPostPage` to `useReducer`.
- Migrate to `next/image`.

## Approach
Incremental fixes starting with Correctness, then Next.js optimizations, then Tailwind styling.

## Rollback Plan
Standard git revert.

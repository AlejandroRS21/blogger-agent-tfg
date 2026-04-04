# Tech Debt Report: Frontend Visual Polish & Dynamic Diversity

**Generated**: 2026-04-04
**Feature**: specs/005-frontend-visual-polish
**Spec Reference**: [spec.md](spec.md)

## Executive Summary

| Severity | Count | Immediate Action Required |
|----------|-------|---------------------------|
| Critical | 0 | None                      |
| Large | 1 | Review Unified Logging    |
| Medium | 1 | Refinement Error Handling |
| Small | 3 | Fixed (Logging migration) |

## Large Issues Requiring Analysis

### [ISSUE-001] Unified Logging Architecture

**Category**: Architecture / Performance
**Location**: `backend/aphra_blogger/agents/`
**Related Spec**: FR-006 (Agent Diversity)
**Constitution Impact**: Principle I (Pipeline Ownership) & Principle III (Verification)

#### Problem Description

Currently, agents use a mix of `print()` and `logging.warning()` for error reporting and flow visibility. In a production/serverless environment (like Modal), `print()` calls are harder to manage, filter, and alert on compared to a structured logging system.

#### Impact if Not Addressed

- Harder debugging in生产环境.
- Inconsistent log levels (Information vs Warning).
- Potential noise in standard output that could interfere with pipe-based tools.

#### Options

**Option 1: Centralized Logger (Recommended)**
- **Approach**: Create an `InternalLogger` utility in `backend/aphra_blogger/utils/` that all agents inherit or use.
- **Pros**: Consistent formatting, easy integration with Modal/Sentry, controllable levels (DEBUG/INFO).
- **Cons**: Requires refactoring all existing print calls.
- **Effort**: M
- **Risk**: Low

**Option 2: Native Python Logging Configuration**
- **Approach**: Standardize using `logging.getLogger(__name__)` and configuration in `main.py`.
- **Pros**: Standardized, no extra dependencies.
- **Cons**: Less custom control for agent-specific metadata.
- **Effort**: S
- **Risk**: Low

#### Recommendation

Implement Option 1 to allow for future metadata enrichment (Agent ID, Run ID) in logs.

---

## Cross-References

- **Tasks**: [tasks.md](tasks.md) (Tech Debt section)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)

## Next Steps

1. Review architecture for Unified Logging.
2. Address TD019 in the next iteration to improve agent resilience.

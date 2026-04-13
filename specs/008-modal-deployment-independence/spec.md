# Feature Specification: Modal Deployment Independence

**Feature Branch**: `[008-modal-deployment-independence]`  
**Created**: 2026-04-09  
**Status**: Draft  
**Input**: User description: "usar modal para el despliegue de agentes y no depender de gemini o openrouter"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Agents Only Through Modal (Priority: P1)

As a platform maintainer, I want all agent deployment and execution flows to run through Modal so that the system has a single, controlled deployment path.

**Why this priority**: This is the core business constraint and directly reduces operational fragmentation and deployment risk.

**Independent Test**: Can be fully tested by deploying and running a representative agent workflow in a clean environment and confirming successful execution without any non-Modal deployment path.

**Acceptance Scenarios**:

1. **Given** a deployable agent workflow, **When** a maintainer performs deployment, **Then** the workflow is deployed and executable through Modal.
2. **Given** a deployment request through a non-Modal path, **When** deployment is attempted, **Then** the system prevents that path and returns actionable guidance.

---

### User Story 2 - Remove Gemini/OpenRouter Dependency (Priority: P2)

As a backend developer, I want the system to run without requiring Gemini or OpenRouter credentials so that environments are simpler and vendor lock-in is reduced.

**Why this priority**: This removes brittle external dependencies and lowers setup friction across development, testing, and production contexts.

**Independent Test**: Can be tested by running end-to-end agent generation in an environment where Gemini/OpenRouter credentials are absent and verifying successful completion.

**Acceptance Scenarios**:

1. **Given** an environment without Gemini and OpenRouter credentials, **When** an agent workflow is executed, **Then** the workflow completes without dependency errors related to those providers.

---

### User Story 3 - Safer Operations and Migration Clarity (Priority: P3)

As an operations owner, I want clear validation messages and migration guidance so that unsupported provider configurations are detected early and corrected quickly.

**Why this priority**: Improves maintainability and reduces production incidents during transition and future onboarding.

**Independent Test**: Can be tested by intentionally providing unsupported provider settings and verifying that users receive clear remediation steps.

**Acceptance Scenarios**:

1. **Given** a configuration that references Gemini or OpenRouter, **When** validation runs, **Then** the system reports the configuration as unsupported and explains the required migration action.

---

### Edge Cases

- What happens when legacy environments still include Gemini/OpenRouter keys even though they are no longer used?
- How does the system behave when Modal is temporarily unavailable during deployment?
- What happens when users try to execute workflows that were previously configured with deprecated provider references?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support agent deployment through Modal as the approved deployment channel for this feature scope.
- **FR-002**: The system MUST prevent deployment attempts that bypass the approved Modal deployment channel.
- **FR-003**: The system MUST execute agent workflows without requiring Gemini credentials.
- **FR-004**: The system MUST execute agent workflows without requiring OpenRouter credentials.
- **FR-005**: The system MUST detect and reject active configurations that declare Gemini or OpenRouter as required runtime dependencies.
- **FR-006**: The system MUST provide clear remediation guidance whenever deprecated provider dependencies are detected.
- **FR-007**: The system MUST preserve functional output parity for core blog generation workflows after dependency removal.
- **FR-008**: The system MUST expose deployment and runtime status outcomes that allow operators to confirm successful Modal execution.

### Key Entities *(include if feature involves data)*

- **Agent Deployment Profile**: Represents a deployable agent configuration, including deployment channel, execution eligibility, and validation state.
- **Provider Dependency Policy**: Represents allowed and disallowed external AI providers for runtime, including policy status and remediation guidance.
- **Workflow Execution Record**: Represents the result of running a content-generation workflow, including completion status, failure reason category, and operator-visible status summary.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of new agent deployments in scope are completed through Modal during acceptance testing.
- **SC-002**: 0 production-critical workflow runs fail due to missing Gemini or OpenRouter credentials after rollout.
- **SC-003**: At least 95% of migrated workflows complete successfully on first run in an environment without Gemini/OpenRouter credentials.
- **SC-004**: Time to diagnose unsupported provider configuration is under 10 minutes for operations users based on provided validation feedback.

## Assumptions

- Platform maintainers and backend developers have permission to deploy and run agent workflows in Modal environments.
- Existing core blog-generation workflows are considered the baseline for functional parity validation.
- Migration targets current and near-term workflows; historic archived outputs are out of scope.
- At least one supported AI provider path (other than Gemini/OpenRouter) is available for all in-scope workflows.

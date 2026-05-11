# Spec: React Doctor Fixes

## Requirements

### R1: Hydration Correctness
- **Description**: The application MUST NOT have hydration mismatches caused by dynamic dates.
- **Scenario**: 
  - Given the homepage renders a post date.
  - When the page is hydrated on the client.
  - Then the date string MUST match what was rendered on the server.
  - Fix: Ensure `toLocaleDateString` is used consistently or date rendering is deferred to client.

### R2: Tailwind 4 Best Practices
- **Description**: The application SHALL use non-default Tailwind palettes and size shorthands.
- **Scenario**:
  - Replace `gray` with `zinc`.
  - Replace `indigo` with `blue` or specific brand colors.
  - Replace `w-N h-N` with `size-N` when both dimensions are equal.

### R3: Next.js Optimization
- **Description**: All images MUST use `next/image` for automatic optimization.
- **Description**: All pages MUST have descriptive metadata.

### R4: State Management
- **Description**: Complex forms with multiple related states MUST use `useReducer`.
- **Target**: `NewPostPage`.

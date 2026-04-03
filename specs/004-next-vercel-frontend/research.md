# Research & Technical Decisions: Frontend Web Application & Cloud Deployment

## Language & Framework
- **Decision**: Next.js 16.1.6 with React 19.2.3 and TypeScript 5.
- **Rationale**: The project docs (`FRONTEND_IMPLEMENTATION.md`) explicitly state this stack is already initialized. Next.js natively supports Static Site Generation (SSG) required by the spec.
- **Alternatives considered**: Plain React (SPA) - rejected because it lacks native SSG and hurts SEO/Lighthouse scores.

## Styling & Design System
- **Decision**: Tailwind CSS 4.
- **Rationale**: Already configured in the frontend directory per established documentation. Allows rapid replication of the target author's design system using utility classes.
- **Alternatives considered**: CSS Modules, Styled Components - rejected to maintain consistency with existing project setup.

## Data Fetching & Storage
- **Decision**: Read static JSON and Markdown/HTML files directly from the `docs/posts` directory during the Next.js build step (using `fs` and `path` modules in Server Components / `getStaticProps`).
- **Rationale**: The backend agents write generated posts to the `docs` folder. Next.js can read these static files at build time to pre-render the pages.
- **Alternatives considered**: Fetching from an external database or API - rejected because the backend outputs static local files, and a database introduces unnecessary complexity.

## Deployment Target
- **Decision**: Vercel.
- **Rationale**: The user explicitly requested Vercel. Vercel provides zero-config deployments for Next.js applications and automatically handles SSG optimizations.
- **Alternatives considered**: Netlify, GitHub Pages (despite Constitution mention of GitHub Pages, Vercel is explicitly requested for this feature branch). *Note: We will configure Vercel to build from the frontend directory but serve files sourced from `docs/`.*

## Testing Framework
- **Decision**: Jest and React Testing Library (Standard Next.js testing).
- **Rationale**: Standard tooling for Next.js unit and component testing.
- **Alternatives considered**: Vitest - rejected to stick to Next.js default recommendations unless otherwise specified.

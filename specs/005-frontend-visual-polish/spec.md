# Feature Specification: Frontend Visual Polish & QA

**Feature Branch**: `005-frontend-visual-polish`  
**Created**: 2026-04-03
**Status**: Completed  
**Input**: User description: "comprobacion de que el fronten funciona perfetamente y todo todo lo que necesita un blog, comprueba todo con el navegador, y soluciona errores visuales y de formato"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Responsive Visual Layout (Priority: P1)

As a reader, I want to experience a visually perfect, distraction-free reading environment across any device so that I can consume AI-generated articles comfortably.

**Why this priority**: A blog's primary value is readability. Formatting errors, broken images, or overflowing text destroy trust and readability.

**Independent Test**: Can be fully tested by opening the application in a desktop browser and resizing the window down to mobile dimensions, verifying that all typography scales correctly and no horizontal scrollbars appear.

**Acceptance Scenarios**:

1. **Given** an article with complex markdown (tables, blockquotes, large images, code blocks), **When** the article is rendered on a mobile screen, **Then** all elements fit within the viewport without breaking the layout.
2. **Given** the blog homepage, **When** scrolling through the list of posts, **Then** the spacing, padding, and hover states match the target design system flawlessly.

---

### User Story 2 - Distinct Structural Archetypes (Priority: P1)

As a long-term reader of JaviPas, I want the AI-generated posts to vary their structure (sometimes opinion-heavy, sometimes purely technical, sometimes quick news flashes) so that the blog feels organic and unpredictable.

**Why this priority**: Correcting the "monotonous template" issue is at the core of mimicking the target blogger's style authentically.

**Independent Test**: Generate 3 different articles on different topics and verify that the HTML structure (heading levels, paragraph distributions, and presence of media) follows distinct patterns.

**Acceptance Scenarios**:

1. **Given** a "Deep Dive" topic, **When** the content is generated, **Then** it includes technical subheadings and explanatory code/list blocks.
2. **Given** a "Quick Opinion" topic, **When** the content is generated, **Then** it presents a short, punchy narrative structure without forced sections.

## Requirements *(mandatory)*

- What happens when an AI-generated post contains exceptionally long words or unbroken URLs? (CSS must gracefully handle `word-break` or `overflow-wrap`).
- How does the system handle missing excerpts or titles in the metadata? (Must provide visually balanced fallbacks).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display all blog post elements (titles, dates, tags, content, images, blockquotes) with perfect alignment and typography spacing according to the `javipas` style profile.
- **FR-002**: System MUST adapt seamlessly to mobile, tablet, and desktop viewports without horizontal scrolling or broken layouts.
- **FR-003**: System MUST include standard blog features such as dynamic `<title>`, `<meta name="description">`, OpenGraph tags, and a favicon.
- **FR-004**: System MUST gracefully handle edge-case text outputs (long strings, large injected LLM iframes) using CSS max-widths and overflow controls.
- **FR-005**: System MUST focus strictly on visual polish of the existing chronological view and post pages, including responsive CSS fixes, basic SEO meta tags, and favicons, without adding new data-driven features like search or related posts.
- **FR-006**: System MUST ensure structural diversity by varying article layouts and "hooks" (opening styles) based on the topic, avoiding predictable post-level sectioning.

### Key Entities 

- **UI Components**: Layout containers, Typography (`prose`), Navigation Bar, Footer.
- **Metadata**: Next.js Metadata objects for SEO and social sharing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 visual overflow errors detected across mobile (320px), tablet (768px), and desktop (1024px+) viewports.
- **SC-002**: 100% of posts evaluate successfully in social sharing debuggers (e.g., proper `<title>` and `<meta>` tags are present).
- **SC-003**: 100% of HTML tags injected by the LLM (like `<table>`, `<img>`, `<pre>`, `<blockquote>`, `<iframe>`) render with styled CSS rather than browser defaults.

## Assumptions

- It is assumed that the overall SSG architecture and data-fetching logic built in feature `004` is structurally sound; this feature focuses strictly on CSS, UX, SEO, and visual polish.
- It is assumed we are strictly relying on Tailwind CSS `prose` (Typography plugin) for rapid textual styling.
- Dark mode behavior should respect the system preference by default (no explicit manual toggle required unless asked).

# Entities: Frontend Web Application & Cloud Deployment

## Context

The data model for the frontend purely reflects the structure of the static files written by the backend. It models the JSON returned by `posts.json` and individual `posts/[slug].json` (or parsed `.html` files).

## Entities

### `Post`
Represents an individual blog article.
- **Attributes**:
  - `slug`: `string` (Required, Primary Key - matches the filename without extension)
  - `title`: `string` (Required - the headline of the article)
  - `date`: `string` (Required - ISO-8601 date string representing publish time)
  - `excerpt`: `string` (Optional - a short summary for the homepage)
  - `content`: `string` (Required - the HTML or Markdown content to be injected)
  - `metadata`: `object` (Optional - dict containing generation statistics like tokens, target profile used, similarity scores from the critic)
- **Relationships**:
  - Part of `PostList` collection.
- **Validation**:
  - `slug` must cleanly map to a URL-safe path segment.
  - `content` must be sanitized or injected safely (via `dangerouslySetInnerHTML` in React if it is pre-sanitized backend output).

### `PostList` (Index)
Represents the collection of metadata for all posts displayed on the homepage root (`/`).
- **Attributes**:
  - `posts`: `Array<PostPreview>` (A lightweight version of Post without the `content` block to minimize payload size during listing).
- **Validation**:
  - Posts must be ordered chronologically descending (newest first).

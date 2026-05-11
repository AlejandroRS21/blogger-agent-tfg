# Post Persistence Specification

## Purpose

Define how generated blog posts are persisted to Supabase PostgreSQL after generation by the Modal webhook.

## Requirements

### Requirement: Post Insert on Generation

The system MUST insert a new post row into Supabase `posts` table immediately after `generate_blog_post.remote()` returns successfully.

The system MUST use fields from `BlogPost` type: `id`, `slug`, `title`, `description`, `content`, `author`, `date`, `word_count`, `reading_time`, `keywords`, `tags`.

The system MUST NOT fail silently — if INSERT fails, the webhook MUST return `success: false` with the error message.

#### Scenario: Successful generation and persist

- GIVEN a valid webhook request with `topic` and `blogger_urls`
- WHEN `generate_blog_post.remote()` returns a result
- THEN system INSERTs post into Supabase `posts` table
- AND webhook returns `{ success: true, data: { slug } }`

#### Scenario: INSERT fails (DB unavailable)

- GIVEN Supabase is unreachable
- WHEN INSERT is attempted after generation
- THEN webhook returns `{ success: false, error: "DB insert failed: <reason>" }`

#### Scenario: Duplicate slug

- GIVEN a post with same slug already exists in `posts`
- WHEN INSERT is attempted
- THEN system UPSERTS (ON CONFLICT slug DO UPDATE) with new data

### Requirement: Post Schema

The `posts` table MUST have columns matching `BlogPost` type exactly:

| Column | Type | Nullable |
|--------|------|----------|
| id | text PRIMARY KEY | NO |
| slug | text UNIQUE | NO |
| title | text | NO |
| description | text | YES |
| content | text | NO |
| author | text | NO |
| date | date | NO |
| word_count | integer | YES |
| reading_time | integer | YES |
| keywords | text[] | YES |
| tags | text[] | YES |
| created_at | timestamptz DEFAULT now() | NO |

#### Scenario: Schema enforcement

- GIVEN a post with missing `content` field
- WHEN INSERT is attempted
- THEN Supabase returns constraint error (NOT NULL violation)

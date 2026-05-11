# Delta for Post Read

## MODIFIED Requirements

### Requirement: Fetch All Posts

The system MUST retrieve all posts from Supabase `posts` table ordered by `date DESC`.
(Previously: fetched from `raw.githubusercontent.com/main/docs/posts.json`)

The system MUST use `@supabase/supabase-js` client initialized with `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

The system MUST return empty array `[]` on fetch error (non-blocking).

#### Scenario: Posts available

- GIVEN Supabase `posts` table has N rows
- WHEN `getAllPosts()` is called
- THEN returns array of N `BlogPost` objects ordered by date DESC

#### Scenario: Supabase unavailable

- GIVEN Supabase is unreachable
- WHEN `getAllPosts()` is called
- THEN logs warning and returns `[]` (page still renders, no crash)

### Requirement: Fetch Single Post by Slug

The system MUST retrieve a single post from Supabase via `.eq('slug', slug)` filter.
(Previously: fetched from `raw.githubusercontent.com/main/docs/posts/{slug}.json`)

#### Scenario: Post exists

- GIVEN a post with slug `"mi-post"` exists in `posts`
- WHEN `fetchPost("mi-post")` is called
- THEN returns the `BlogPost` object

#### Scenario: Post not found

- GIVEN no post with slug `"nonexistent"` exists
- WHEN `fetchPost("nonexistent")` is called
- THEN returns `null`

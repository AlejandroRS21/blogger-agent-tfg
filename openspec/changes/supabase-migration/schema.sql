-- Schema for blogger-agent-tfg posts
-- Run in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS posts (
  id            text PRIMARY KEY,
  slug          text UNIQUE NOT NULL,
  title         text NOT NULL,
  description   text,
  content       text NOT NULL,
  author        text NOT NULL DEFAULT 'Blogger Agent',
  date          date NOT NULL,
  word_count    integer,
  reading_time  integer,
  keywords      text[],
  tags          text[],
  cover_image_url text,
  created_at    timestamptz DEFAULT now()
);

-- Public read policy (TFG demo — no auth)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read" ON posts
  FOR SELECT USING (true);

CREATE POLICY "Service role write" ON posts
  FOR ALL USING (auth.role() = 'service_role');

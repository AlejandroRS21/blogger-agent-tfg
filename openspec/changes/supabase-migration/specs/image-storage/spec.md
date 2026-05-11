# Image Storage Specification

## Purpose

Define how images are stored in Supabase Storage bucket and their URLs linked to posts.

## Requirements

### Requirement: Public Image Bucket

The system MUST use a Supabase Storage bucket named `post-images` configured as public.

The bucket MUST allow anonymous read access (CDN URLs accessible without auth).

#### Scenario: Bucket access

- GIVEN a file uploaded to `post-images/` bucket
- WHEN a GET request is made to the CDN URL
- THEN the image is returned without authentication

### Requirement: Image URL in Post

The `posts` table SHOULD have a `cover_image_url` column (text, nullable) storing the CDN URL of the cover image.

The system MAY leave `cover_image_url` null if no image is generated during the current workflow.

#### Scenario: Post without image

- GIVEN Modal webhook completes generation without image upload
- WHEN post is inserted into `posts`
- THEN `cover_image_url` is NULL
- AND post is still valid and readable

#### Scenario: Future image upload

- GIVEN `cover_image_url` is null
- WHEN an image is later uploaded to `post-images/{slug}/cover.jpg`
- THEN `posts` row is updated with the CDN URL

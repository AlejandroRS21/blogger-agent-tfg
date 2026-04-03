import { z } from 'zod';

/**
 * Zod schema to validate post data from posts.json
 * This ensures the UI has the required fields before rendering.
 */
export const PostListItemSchema = z.object({
  slug: z.string().min(1, "Slug is required"),
  title: z.string().min(1, "Title is required"),
  date: z.string().optional().default(() => new Date().toISOString()),
  excerpt: z.string().optional().default(""),
});

export type PostListItem = z.infer<typeof PostListItemSchema>;

/**
 * Post Metadata schema for additional info like keywords, sentiment, etc.
 * z.record(z.unknown()) defines a record with string keys and unknown values.
 */
export const PostMetadataSchema = z.record(z.string(), z.unknown());
export type PostMetadata = z.infer<typeof PostMetadataSchema>;

/**
 * Zod schema to validate individual post document (the JSON files in docs/posts/)
 */
export const PostDocumentSchema = z.object({
  title: z.string().min(1, "Post title is required"),
  content: z.string().min(1, "Content is required"),
  metadata: PostMetadataSchema.optional(),
  date: z.string().optional(),
  excerpt: z.string().optional(),
});

export type PostDocument = z.infer<typeof PostDocumentSchema>;

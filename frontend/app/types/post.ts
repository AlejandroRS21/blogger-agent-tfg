import { z } from 'zod';

/**
 * Validated Zod Schema for a single Blog Post.
 * Used for both individual post files and individual elements in the main catalog.
 */
export const PostSchema = z.object({
  id: z.string().optional(),
  slug: z.string().min(1, "Slug is required").or(z.string().optional().transform((_, ctx) => (ctx as any).id)).pipe(z.string().min(1)),
  title: z.string().min(1, "Post Title is required").default("Post sin título"),
  date: z.string().optional().default(() => new Date().toISOString()),
  excerpt: z.string().optional().default("Sin descripción disponible."),
  content: z.string().optional().default(""),
  tags: z.array(z.string()).optional().default([]),
  image: z.string().optional(),
  author: z.string().optional().default("Javi Pas"),
});

/**
 * Validated Zod Schema for the complete posts catalog (posts.json).
 */
export const PostsCatalogSchema = z.array(PostSchema);

export type Post = z.infer<typeof PostSchema>;

// Internal compatibility types (matches existing api.ts usage)
export const PostListItemSchema = z.object({
  slug: z.string().min(1),
  title: z.string(),
  date: z.string(),
  excerpt: z.string(),
});

export const PostDocumentSchema = z.object({
  title: z.string(),
  content: z.string(),
  metadata: z.record(z.string(), z.any()).optional(),
  date: z.string().optional(),
  excerpt: z.string().optional(),
});

export type PostListItem = z.infer<typeof PostListItemSchema>;
export type PostDocument = z.infer<typeof PostDocumentSchema>;

// Fix legacy component requirements
export type PostMetadata = Record<string, any>;

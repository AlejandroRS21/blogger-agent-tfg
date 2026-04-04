import fs from 'fs';
import path from 'path';
import { PostSchema, PostsCatalogSchema, Post, PostDocumentSchema, PostDocument } from '../types/post';

const DATA_DIR = path.join(process.cwd(), '../docs');
const POSTS_DIR = path.join(DATA_DIR, 'posts');

/**
 * Common data normalization to prevent build/runtime crashes.
 */
function normalizePost(post: any): Post {
  // Ensure we have a valid slug from internal ID or fileName if slug is missing
  const slug = post.slug || post.id || "unnamed-post";
  
  const parsed = PostSchema.safeParse({
    ...post,
    slug,
    // Clean potential AI artifacts (backticks in title/excerpt)
    title: post.title?.replace(/`/g, '') || "Post sin título",
    excerpt: post.excerpt?.replace(/`/g, '') || "Sin descripción disponible."
  });

  if (!parsed.success) {
    console.warn(`[API] Validation failed for post: ${slug}`, parsed.error.format());
    return {
      slug,
      title: post.title || "Post inválido",
      date: new Date().toISOString(),
      excerpt: "Error en validación de datos.",
      content: "",
      tags: [],
      author: "Sistema"
    };
  }
  return parsed.data;
}

export async function getPosts(): Promise<Post[]> {
  try {
    const filePath = path.join(DATA_DIR, 'posts.json');
    if (!fs.existsSync(filePath)) {
      console.warn(`[API] posts.json not found at ${filePath}`);
      return [];
    }
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(fileContents);
    
    const catalog = Array.isArray(data) ? data : (data.posts || []);
    return catalog.map(normalizePost);
  } catch (error) {
    console.error('[API] Error reading posts catalog:', error);
    return [];
  }
}

export async function getPostBySlug(slug: string): Promise<PostDocument | null> {
  if (!slug) return null;
  
  try {
    // Check for .json or .html versions
    const jsonPath = path.join(POSTS_DIR, `${slug}.json`);
    const htmlPath = path.join(POSTS_DIR, `${slug}.html`);

    if (fs.existsSync(jsonPath)) {
      const fileContents = fs.readFileSync(jsonPath, 'utf8');
      const data = JSON.parse(fileContents);
      
      const parsed = PostDocumentSchema.safeParse({
        ...data,
        content: data.content || data.body || "",
        title: data.title || slug
      });

      if (!parsed.success) {
         console.warn(`[API] Invalid Document for ${slug}`, parsed.error.format());
         return null;
      }
      return parsed.data;
    } 
    
    if (fs.existsSync(htmlPath)) {
      const content = fs.readFileSync(htmlPath, 'utf8');
      return {
        title: slug.replace(/-/g, ' '),
        content: content,
        date: new Date().toISOString()
      };
    }

    return null;
  } catch (error) {
    console.error(`[API] Error fetching post ${slug}:`, error);
    return null;
  }
}

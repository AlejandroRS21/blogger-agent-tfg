import fs from 'fs/promises';
import path from 'path';
import { PostListItem, PostDocument } from '../types/post';

const DOCS_DIR = path.join(process.cwd(), '..', 'docs');
const POSTS_JSON_PATH = path.join(DOCS_DIR, 'posts.json');
const POSTS_DIR = path.join(DOCS_DIR, 'posts');

export async function getAllPosts(): Promise<PostListItem[]> {
  try {
    const fileContents = await fs.readFile(POSTS_JSON_PATH, 'utf8');
    const data = JSON.parse(fileContents);
    
    // Some formats might wrap in { posts: [...] }, or just return an array.
    if (Array.isArray(data)) {
      return data;
    } else if (data.posts && Array.isArray(data.posts)) {
      return data.posts;
    }
    
    return [];
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      console.warn(`[api] posts.json not found at ${POSTS_JSON_PATH}. Returning empty list.`);
      return [];
    }
    console.error('[api] Failed to read posts.json:', error);
    return [];
  }
}

export async function getPostBySlug(slug: string): Promise<PostDocument | null> {
  // Prevent directory traversal attacks
  const safeSlug = path.basename(slug);
  const jsonPath = path.join(POSTS_DIR, `${safeSlug}.json`);
  const htmlPath = path.join(POSTS_DIR, `${safeSlug}.html`);

  try {
    // Attempt JSON first
    const jsonContent = await fs.readFile(jsonPath, 'utf8');
    const data = JSON.parse(jsonContent);
    return data as PostDocument;
  } catch {
    console.warn(`[api] Post JSON for slug ${safeSlug} not found. Trying HTML...`);
    
    try {
      // Fallback to HTML if available
      const htmlContent = await fs.readFile(htmlPath, 'utf8');
      
      // Fallback matching logic (very rudimentary, assume it's just raw markup for now)
      return {
        title: safeSlug.replace(/-/g, ' '), // Guessing title
        content: htmlContent,
      };
    } catch {
      console.error(`[api] Post resource not found for ${safeSlug}`);
      return null;
    }
  }
}

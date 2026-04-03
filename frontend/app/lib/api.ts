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
    
    let rawPosts = [];
    // Some formats might wrap in { posts: [...] }, or just return an array.
    if (Array.isArray(data)) {
      rawPosts = data;
    } else if (data.posts && Array.isArray(data.posts)) {
      rawPosts = data.posts;
    }
    
    // Normalize data to ensure `slug` and `excerpt` exist
    return rawPosts.map((item: any) => {
      let title = item.title || 'Sin Título';
      let excerpt = item.excerpt || item.description || '';

      // Handle AI encoded JSON in titles
      if (title.includes('topic_out') && title.startsWith('{')) {
        try {
          const cleaned = title.replace(/'/g, '"');
          const parsed = JSON.parse(cleaned);
          title = parsed.topic_out || parsed.title || title;
        } catch (e) {
          console.warn('[api] Failed to parse JSON title', e);
        }
      }

      // Handle AI encoded markdown in excerpts
      excerpt = excerpt.replace(/```markdown\s*/g, '').replace(/```\s*/g, '').replace(/^#+\s+.*/g, '').trim();

      return {
        slug: item.slug || item.id || '',
        title,
        date: item.date || new Date().toISOString(),
        excerpt: excerpt.substring(0, 200) + (excerpt.length > 200 ? '...' : '')
      };
    }).filter((post: PostListItem) => post.slug !== '');
    
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
    
    return {
      title: data.title || safeSlug,
      content: data.html_code || data.content || '',
      metadata: data.metadata || {},
      date: data.date || data.metadata?.date,
      excerpt: data.description || data.excerpt
    } as PostDocument;
  } catch {
    console.warn(`[api] Post JSON for slug ${safeSlug} not found. Trying HTML...`);
    
    try {
      // Fallback to HTML if available
      const htmlContent = await fs.readFile(htmlPath, 'utf8');
      
      // Fallback matching logic
      return {
        title: safeSlug.replace(/-/g, ' '),
        content: htmlContent,
      };
    } catch {
      console.error(`[api] Post resource not found for ${safeSlug}`);
      return null;
    }
  }
}

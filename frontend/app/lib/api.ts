import fs from 'fs/promises';
import path from 'path';
import { 
  PostListItem, 
  PostDocument, 
  PostListItemSchema, 
  PostDocumentSchema 
} from '../types/post';

const DOCS_DIR = path.resolve(process.cwd(), '..', 'docs');
const POSTS_JSON_PATH = path.join(DOCS_DIR, 'posts.json');
const POSTS_DIR = path.join(DOCS_DIR, 'posts');

export async function getAllPosts(): Promise<PostListItem[]> {
  try {
    const fileContents = await fs.readFile(POSTS_JSON_PATH, 'utf8');
    const data = JSON.parse(fileContents);
    
    let rawPosts: any[] = [];
    if (Array.isArray(data)) {
      rawPosts = data;
    } else if (data.posts && Array.isArray(data.posts)) {
      rawPosts = data.posts;
    }
    
    const processedPosts = rawPosts.map((item: any) => {
      const slug = (item.slug || item.id || "").toString().trim();
      let title = (item.title || "").toString().trim();
      let excerpt = (item.excerpt || item.description || "").toString().trim();

      if (title.startsWith('{')) {
        try {
          const parsed = JSON.parse(title.replace(/'/g, '"'));
          title = parsed.topic_out || parsed.title || title;
        } catch {}
      }

      excerpt = excerpt.replace(/```markdown\s*/g, '').replace(/```\s*/g, '').replace(/^#+\s+.*/g, '').trim();
      if (excerpt.length > 200) excerpt = excerpt.substring(0, 197) + "...";

      const normalizedPost = {
        slug,
        title: title || "Post sin título",
        date: item.date || new Date().toISOString(),
        excerpt: excerpt || "Sin resumen disponible."
      };

      const result = PostListItemSchema.safeParse(normalizedPost);
      if (!result.success) {
        console.error(`[api] Validation failed for post: ${slug}`);
        return null;
      }
      return result.data;
    });

    return processedPosts.filter((post: PostListItem | null): post is PostListItem => post !== null);
    
  } catch (error) {
    if ((error as any).code === 'ENOENT') {
      console.warn(`[api] posts.json not found at ${POSTS_JSON_PATH}. Returning empty list.`);
      return [];
    }
    console.error('[api] Unexpected error reading posts.json:', error);
    return [];
  }
}

export async function getPostBySlug(slug: string): Promise<PostDocument | null> {
  const safeSlug = path.basename(slug);
  const jsonPath = path.join(POSTS_DIR, `${safeSlug}.json`);

  try {
    const jsonContent = await fs.readFile(jsonPath, 'utf8');
    const rawData = JSON.parse(jsonContent);
    
    const mappedData = {
      title: rawData.title || safeSlug.replace(/-/g, ' '),
      content: rawData.html_code || rawData.content || "",
      metadata: rawData.metadata || {},
      date: rawData.date || rawData.metadata?.date,
      excerpt: rawData.description || rawData.excerpt
    };

    const result = PostDocumentSchema.safeParse(mappedData);
    if (!result.success) {
      console.error(`[api] Invalid post document format for ${safeSlug}`);
      return null;
    }
    
    return result.data;
  } catch (error) {
    console.warn(`[api] Post JSON for slug ${safeSlug} not found or invalid.`);
    
    const htmlPath = path.join(POSTS_DIR, `${safeSlug}.html`);
    try {
      const htmlContent = await fs.readFile(htmlPath, 'utf8');
      return {
        title: safeSlug.replace(/-/g, ' '),
        content: htmlContent,
      };
    } catch {
      return null;
    }
  }
}

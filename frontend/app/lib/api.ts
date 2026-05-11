import { PostSchema, Post, PostDocumentSchema, PostDocument } from '../types/post';

const GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AlejandroRS21/blogger-agent-tfg/main/docs";

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

export async function getAllPosts(): Promise<Post[]> {
  try {
    const url = `${GITHUB_RAW_BASE}/posts.json`;
    const response = await fetch(url, { next: { revalidate: 60 } }); // Cache 1 minute
    
    if (!response.ok) {
      console.warn(`[API] Failed to fetch catalog from ${url}: ${response.statusText}`);
      return [];
    }
    
    const data = await response.json();
    const catalog = Array.isArray(data) ? data : (data.posts || []);
    return catalog.map(normalizePost);
  } catch (error) {
    console.error('[API] Error fetching posts catalog:', error);
    return [];
  }
}

export async function getPostBySlug(slug: string): Promise<PostDocument | null> {
  if (!slug) return null;
  
  const jsonUrl = `${GITHUB_RAW_BASE}/posts/${slug}.json`;
  const htmlUrl = `${GITHUB_RAW_BASE}/posts/${slug}.html`;

  // Try JSON first
  try {
    const response = await fetch(jsonUrl, { next: { revalidate: 60 } });
    
    if (response.ok) {
      const data = await response.json();
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
    
    // If JSON not found (404), try HTML
    if (response.status === 404) {
      const htmlResponse = await fetch(htmlUrl, { next: { revalidate: 60 } });
      if (htmlResponse.ok) {
        const content = await htmlResponse.text();
        return {
          title: slug.replace(/-/g, ' '),
          content: content,
          date: new Date().toISOString()
        };
      }
    }

    return null;
  } catch (error) {
    console.error(`[API] Error fetching post ${slug}:`, error);
    return null;
  }
}

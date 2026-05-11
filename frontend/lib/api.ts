import type { BlogPost } from "@/types/post";

// Note: post generation was moved to app/posts/new/page.tsx which calls the Modal webhook directly.
// This module only handles reading posts from the GitHub-hosted docs/ directory.

// Generate static sample posts for homepage display
export function getSamplePosts(): BlogPost[] {
  return [];
}

export async function getAllPosts(): Promise<BlogPost[]> {
  try {
    const GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AlejandroRS21/blogger-agent-tfg/main/docs";
    const response = await fetch(`${GITHUB_RAW_BASE}/posts.json`, { next: { revalidate: 60 } });

    if (!response.ok) {
      return [];
    }

    const data = await response.json();
    return data.map((post: any) => ({
      ...post,
      slug: post.slug || post.id || "unnamed-post",
      title: post.title || "Post sin título",
      date: post.date || new Date().toISOString(),
      author: post.author || "Blogger Agent",
    }));
  } catch (error) {
    console.warn("[API] Failed to fetch posts:", error);
    return [];
  }
}

export async function fetchPost(slug: string): Promise<BlogPost | null> {
  try {
    const GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AlejandroRS21/blogger-agent-tfg/main/docs";
    const response = await fetch(`${GITHUB_RAW_BASE}/posts/${slug}.json`, { next: { revalidate: 60 } });

    if (response.ok) {
      return await response.json();
    }

    return null;
  } catch {
    return null;
  }
}

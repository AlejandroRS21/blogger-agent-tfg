import type { BlogPost } from "@/types/post";
import { supabase } from "./supabase";

// Note: post generation happens in app/posts/new/page.tsx (Modal webhook).
// This module handles reading posts from Supabase.

export async function getAllPosts(): Promise<BlogPost[]> {
  try {
    const { data, error } = await supabase
      .from("posts")
      .select("*")
      .order("date", { ascending: false });

    if (error) {
      console.warn("[API] Supabase error fetching posts:", error.message);
      return [];
    }

    return (data ?? []) as BlogPost[];
  } catch (err) {
    console.warn("[API] Failed to fetch posts:", err);
    return [];
  }
}

export async function fetchPost(slug: string): Promise<BlogPost | null> {
  try {
    const { data, error } = await supabase
      .from("posts")
      .select("*")
      .eq("slug", slug)
      .single();

    if (error) {
      console.warn(`[API] Supabase error fetching post "${slug}":`, error.message);
      return null;
    }

    return data as BlogPost;
  } catch {
    return null;
  }
}

/** @deprecated — kept for backward compat, returns empty array */
export function getSamplePosts(): BlogPost[] {
  return [];
}

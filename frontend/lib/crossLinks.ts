/**
 * Cross-linking engine for blog posts.
 *
 * Scans HTML content and auto-links phrases that match other post titles.
 * This creates the classic blog feature where mentioning a topic
 * automatically links to its dedicated post.
 *
 * Algorithm:
 * 1. Fetch all post titles + slugs (cached)
 * 2. Sort by title length descending (longest match first)
 * 3. For each text node outside existing HTML tags, replace matching
 *    phrases with anchored links
 */

import { getAllPosts } from "./api";

export interface TitleLink {
  title: string;
  slug: string;
}

// In-memory cache for the title map (resets on page reload, fine for SSR)
let titleLinksCache: TitleLink[] | null = null;

export async function getTitleLinks(): Promise<TitleLink[]> {
  if (titleLinksCache) return titleLinksCache;

  const posts = await getAllPosts();
  titleLinksCache = posts.map((p) => ({ title: p.title, slug: p.slug }));
  return titleLinksCache;
}

/**
 * Apply cross-links to HTML content.
 *
 * @param html - Raw HTML content of the post
 * @param currentSlug - Current post slug (to avoid self-linking)
 * @param links - Title/link pairs from getTitleLinks()
 * @returns HTML with cross-links injected
 */
export function applyCrossLinks(
  html: string,
  currentSlug: string,
  links: TitleLink[]
): string {
  // Sort descending by title length so "Paella Valenciana" matches before "Paella"
  const sorted = [...links]
    .filter((l) => l.slug !== currentSlug)
    .sort((a, b) => b.title.length - a.title.length);

  if (sorted.length === 0) return html;

  let result = html;

  for (const { title, slug } of sorted) {
    const escaped = title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`\\b${escaped}\\b`, "gi");

    result = result.replace(regex, (match, offset: number) => {
      // Don't link if already inside an <a> tag
      const before = result.substring(0, offset);
      const lastLinkOpen = before.lastIndexOf("<a ");
      const lastLinkClose = before.lastIndexOf("</a>");

      if (lastLinkOpen > lastLinkClose) {
        return match; // already linked
      }

      // Don't link if inside any other HTML tag (attribute values, etc.)
      const lastTagOpen = before.lastIndexOf("<");
      const lastTagClose = before.lastIndexOf(">");
      if (lastTagOpen > lastTagClose) {
        return match; // inside an HTML tag
      }

      return `<a href="/posts/${slug}" class="font-medium text-blue-600 underline decoration-blue-300 decoration-2 underline-offset-2 transition-colors hover:text-blue-800">${match}</a>`;
    });
  }

  return result;
}

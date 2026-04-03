export interface PostMetadata {
  style_score?: number;
  structural_variance?: number;
  [key: string]: unknown;
}

export interface PostListItem {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
}

export interface PostListResponse {
  posts: PostListItem[];
}

export interface PostDocument {
  title: string;
  content: string; // HTML markup
  metadata?: PostMetadata;
  // added for fallback metadata parsing from html if necessary
  date?: string;
  excerpt?: string;
}

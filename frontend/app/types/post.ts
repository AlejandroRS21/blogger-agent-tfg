/**
 * TypeScript types for blog posts
 */

export interface BlogPost {
  id: string;
  title: string;
  description: string;
  html_code: string;
  metadata: {
    word_count: number;
    reading_time: number;
    date: string;
    author?: string;
    tags?: string[];
  };
  images?: {
    url: string;
    alt: string;
    credit?: string;
  }[];
}

export interface GenerateRequest {
  blogger_name: string;
  blogger_bio: string;
  blogger_sample_posts: string[];
  topic: string;
  keywords?: string[];
}

export interface GenerateResponse {
  success: boolean;
  post?: BlogPost;
  error?: string;
  execution_time?: number;
}

import Link from 'next/link';
import { PostListItem } from '../types/post';

interface Props {
  post: PostListItem;
}

/**
 * PostCard Component
 * 
 * Displays a summary of a blog post in the list view.
 * Mimics the clean, typography-focused style of javipas.com.
 */
export default function PostCard({ post }: Props) {
  // Safe date formatting
  const dateObj = post.date ? new Date(post.date) : new Date();
  const formattedDate = dateObj.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  // Use a fallback if slug is missing (though Zod should prevent this)
  const postHref = post.slug ? `/posts/${post.slug}` : '#';

  return (
    <article className="group py-12 border-b border-zinc-100 dark:border-zinc-900 last:border-0 hover:bg-zinc-50/50 dark:hover:bg-zinc-900/50 transition-colors px-4 -mx-4 rounded-xl">
      <Link href={postHref} className="flex flex-col gap-4 no-underline group-hover:no-underline">
        
        <header className="flex flex-col gap-2">
          <div className="flex items-center gap-3 text-[10px] font-black uppercase tracking-widest text-accent">
            <time dateTime={post.date}>{formattedDate}</time>
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            <span className="text-secondary/60">Post IA</span>
          </div>
          
          <h2 className="text-2xl md:text-4xl font-black tracking-tighter text-primary group-hover:text-accent transition-colors leading-[1.1]">
            {post.title}
          </h2>
        </header>

        <p className="text-secondary dark:text-zinc-400 leading-relaxed font-medium line-clamp-3 text-sm md:text-base">
          {post.excerpt}
        </p>
        
        <footer className="mt-2 flex items-center gap-1 text-accent font-bold text-xs uppercase tracking-widest group-hover:gap-2 transition-all">
          <span>Leer artículo</span>
          <span className="text-lg">→</span>
        </footer>
      </Link>
    </article>
  );
}

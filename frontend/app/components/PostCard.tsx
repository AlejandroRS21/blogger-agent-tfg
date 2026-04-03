import Link from 'next/link';
import { PostListItem } from '../types/post';

interface Props {
  post: PostListItem;
}

export default function PostCard({ post }: Props) {
  const formattedDate = new Date(post.date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <article className="group py-10 border-b border-zinc-100 dark:border-zinc-900 last:border-0">
      <Link href={`/posts/${post.slug}`} className="flex flex-col gap-3">
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight text-primary group-hover:text-accent transition-colors leading-tight">
          {post.title}
        </h2>
        
        <div className="flex items-center gap-3 text-[10px] font-black uppercase tracking-widest text-secondary/60">
          <time dateTime={post.date}>{formattedDate}</time>
          <span className="h-1 w-1 rounded-full bg-accent" />
          <span>Post IA</span>
        </div>

        <p className="text-secondary dark:text-secondary leading-relaxed font-medium line-clamp-2 italic">
          {post.excerpt}
        </p>
        
        <div className="mt-2 flex items-center gap-1 text-accent font-bold text-sm">
          <span>Leer artículo</span>
          <span className="group-hover:translate-x-1 transition-transform">→</span>
        </div>
      </Link>
    </article>
  );
}

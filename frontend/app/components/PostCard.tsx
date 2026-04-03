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
    <article className="py-6 border-b border-gray-200 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors px-4 -mx-4 rounded-lg">
      <Link href={`/posts/${post.slug}`} className="block block-hover">
        <h2 className="text-xl md:text-2xl font-bold mb-2 leading-tight">
          {post.title}
        </h2>
        <div className="text-gray-500 dark:text-gray-400 text-sm mb-3">
          {formattedDate}
        </div>
        <p className="text-gray-700 dark:text-gray-300 line-clamp-3">
          {post.excerpt}
        </p>
      </Link>
    </article>
  );
}

import { getAllPosts } from './lib/api';
import PostCard from './components/PostCard';

export const dynamic = 'force-static';
export const revalidate = false;

export default async function Home() {
  const posts = await getAllPosts();

  if (!posts || posts.length === 0) {
    return (
      <div className="py-20 text-center">
        <h2 className="text-2xl font-semibold mb-4">Aún no hay publicaciones</h2>
        <p className="text-gray-500">El agente no ha generado ningún artículo todavía.</p>
      </div>
    );
  }

  // Sort by date (newest first)
  const sortedPosts = posts.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return (
    <div className="space-y-4">
      {sortedPosts.map((post) => (
        <PostCard key={post.slug} post={post} />
      ))}
    </div>
  );
}

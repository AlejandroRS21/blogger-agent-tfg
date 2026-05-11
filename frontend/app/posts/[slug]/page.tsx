import { getPostBySlug, getAllPosts } from '../../lib/api';
import HTMLRenderer from '../../components/HTMLRenderer';
import PostMeta from '../../components/PostMeta';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

interface Params {
  slug: string;
}

export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPostBySlug(slug);
  
  if (!post) return { title: 'Post No Encontrado' };

  return {
    title: `${post.title} | BloggerIA`,
    description: post.excerpt || `Lee el último artículo sobre ${post.title}`,
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
    }
  };
}

export default async function PostPage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  // Safety check
  if (!slug) return notFound();

  const post = await getPostBySlug(slug);

  if (!post) {
    return notFound();
  }

  // Use metadata or fallbacks
  const postDate = post.date || (post.metadata?.date as string);
  const displayDate = postDate ? new Date(postDate).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }) : null;

  return (
    <article className="max-w-4xl mx-auto px-4 py-12">
      <header className="mb-10 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-foreground mb-4 leading-tight tracking-tight">
          {post.title}
        </h1>
        {displayDate && (
          <div className="text-muted-foreground font-medium mb-4">
            {displayDate}
          </div>
        )}
      </header>

      <div className="prose-container bg-card/30 rounded-2xl p-6 md:p-10 border border-border/50 shadow-xl backdrop-blur-sm">
        <HTMLRenderer html={post.content} />
      </div>

      {post.metadata && Object.keys(post.metadata).length > 0 && (
        <div className="mt-12">
           <PostMeta metadata={post.metadata} />
        </div>
      )}

      <footer className="mt-16 pt-8 border-t border-border/40 text-sm text-muted-foreground flex justify-between items-center">
        <div>Generado por el motor de agentes de BloggerIA</div>
        <div className="flex gap-4 italic opacity-70">
           {post.excerpt && <span>{post.excerpt.slice(0, 100)}...</span>}
        </div>
      </footer>
    </article>
  );
}

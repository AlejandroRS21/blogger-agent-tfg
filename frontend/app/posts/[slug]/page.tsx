import { notFound } from 'next/navigation';
import { getAllPosts, getPostBySlug } from '../../lib/api';
import HTMLRenderer from '../../components/HTMLRenderer';
import PostMeta from '../../components/PostMeta';
import Link from 'next/link';

import type { Metadata } from 'next';

export const dynamic = 'force-static';
export const dynamicParams = false;

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata(props: Props): Promise<Metadata> {
  const params = await props.params;
  const post = await getPostBySlug(params.slug);
  
  if (!post) return { title: 'Post no encontrado' };

  return {
    title: `${post.title} | AI Blogger`,
    description: post.excerpt || `Lee sobre ${post.title} en nuestro blog generado por IA.`,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.date,
    }
  };
}

export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function PostPage(props: Props) {
  const params = await props.params;
  const post = await getPostBySlug(params.slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="py-10 max-w-[65ch] mx-auto">
      <header className="mb-12">
        <Link href="/" className="group inline-flex items-center gap-2 text-sm font-bold text-accent mb-8 hover:no-underline">
          <span className="group-hover:-translate-x-1 transition-transform">←</span>
          <span>Volver al inicio</span>
        </Link>
        
        <h1 className="text-4xl md:text-5xl font-black tracking-tighter mb-6 leading-[1.1] text-primary">
          {post.title}
        </h1>
        
        {post.date && (
          <div className="flex items-center gap-3 text-xs font-bold uppercase tracking-widest text-secondary">
            <time dateTime={post.date}>
              {new Date(post.date).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </time>
            <span className="h-1 w-1 rounded-full bg-accent" />
            <span>Escrito por Blogger Agent</span>
          </div>
        )}
      </header>

      <div className="prose dark:prose-invert prose-zinc max-w-none">
        <HTMLRenderer htmlContent={post.content} />
      </div>

      <PostMeta metadata={post.metadata} />
      
      <footer className="mt-16 pt-8 border-t border-zinc-100 dark:border-zinc-900">
        <Link href="/" className="text-secondary hover:text-accent font-bold text-sm">
          ¿Te ha gustado? Descubre más artículos →
        </Link>
      </footer>
    </article>
  );
}

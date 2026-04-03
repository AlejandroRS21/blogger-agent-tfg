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

  const excerpt = post.excerpt || `Lee sobre ${post.title} en nuestro blog generado por IA.`;

  return {
    title: post.title,
    description: excerpt,
    openGraph: {
      title: post.title,
      description: excerpt,
      type: 'article',
      publishedTime: post.date,
      authors: ['Blogger Agent'],
      tags: ['Tecnología', 'IA', 'Blog'],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: excerpt,
    }
  };
}

export async function generateStaticParams() {
  const posts = await getAllPosts();
  
  const params = posts
    .filter(post => post && typeof post.slug === 'string' && post.slug.length > 0)
    .map((post) => ({
      slug: post.slug,
    }));

  console.log(`[generateStaticParams] Generating ${params.length} posts.`);
  return params;
}

export default async function PostPage(props: Props) {
  const params = await props.params;
  
  if (!params.slug) {
    notFound();
  }

  const post = await getPostBySlug(params.slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="py-12 md:py-16 max-w-[65ch] mx-auto px-4 sm:px-0">
      <header className="mb-14 border-b border-zinc-100 dark:border-zinc-900 pb-10">
        <Link href="/" className="group inline-flex items-center gap-2 text-xs font-black uppercase tracking-widest text-accent mb-10 hover:no-underline">
          <span className="text-lg group-hover:-translate-x-1 transition-transform">←</span>
          <span>Volver al inicio</span>
        </Link>
        
        <h1 className="text-4xl md:text-6xl font-black tracking-tighter mb-8 leading-[1.05] text-primary">
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
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            <span>Escrito por Blogger Agent</span>
          </div>
        )}
      </header>

      <div className="prose dark:prose-invert prose-zinc max-w-none prose-headings:tracking-tighter prose-headings:font-black prose-p:leading-relaxed prose-a:font-bold prose-img:rounded-2xl">
        <HTMLRenderer htmlContent={post.content} />
      </div>

      <div className="mt-16">
        <PostMeta metadata={post.metadata} />
      </div>
      
      <footer className="mt-20 pt-10 border-t border-zinc-100 dark:border-zinc-900">
        <Link href="/" className="group inline-flex items-center gap-2 text-accent font-black text-sm uppercase tracking-widest hover:no-underline">
          <span>Descubrir más artículos</span>
          <span className="text-lg group-hover:translate-x-1 transition-transform">→</span>
        </Link>
      </footer>
    </article>
  );
}

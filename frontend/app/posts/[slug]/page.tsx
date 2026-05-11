import Link from "next/link";
import { notFound } from "next/navigation";
import { getPostBySlug, getAllPosts } from '../../lib/api';
import HTMLRenderer from '../../components/HTMLRenderer';
import { Metadata } from 'next';
import Image from 'next/image';

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
      images: post.image ? [post.image] : [],
    }
  };
}

export default async function PostPage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
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

  const readingTime = (post as any).meta?.reading_time || 5;
  const wordCount = (post as any).meta?.word_count || 1200;
  const author = post.author || "IA Agent";
  const tags = post.tags || [];

  return (
    <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
      {/* Navigation */}
      <div className="mb-10 flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Volver al inicio
        </Link>

        <Link
          href="/posts/new"
          className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
        >
          Generar otro
        </Link>
      </div>

      {/* Main Container */}
      <article className="mx-auto max-w-3xl">
        {/* Header info */}
        <header className="mb-8 border-b border-gray-200 pb-6">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            {post.title}
          </h1>

          <div className="mt-4 flex flex-wrap items-center gap-4 text-sm text-gray-500">
            <span className="font-medium text-gray-700">{author}</span>
            <span className="text-gray-300">|</span>
            <span>{displayDate}</span>
            <span className="text-gray-300">|</span>
            <span>{readingTime} min de lectura</span>
            <span className="text-gray-300">|</span>
            <span>{wordCount} palabras</span>
          </div>

          {tags.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </header>

        {/* Featured Image */}
        {post.image ? (
          <div className="relative mb-10 h-72 w-full overflow-hidden rounded-2xl md:h-96">
            <Image
              src={post.image}
              alt={post.title}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, 800px"
              priority
            />
          </div>
        ) : (
          <div className="relative mb-10 flex h-48 w-full items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-100">
            <div className="text-center">
              <span className="text-4xl">🤖</span>
              <p className="mt-2 text-sm font-medium text-blue-800 opacity-80">BloggerIA</p>
            </div>
          </div>
        )}

        {/* Blog content with prose styles */}
        <div className="prose max-w-none text-gray-800 prose-headings:text-gray-900 prose-a:text-blue-600">
          <HTMLRenderer html={post.content} />
        </div>

        {/* Meta keywords */}
        {(post as any).meta?.keywords && (post as any).meta.keywords.length > 0 && (
          <div className="mt-10 border-t border-gray-200 pt-6">
            <p className="text-xs text-gray-500">
              Palabras clave:{" "}
              <span className="text-gray-700">{(post as any).meta.keywords.join(", ")}</span>
            </p>
          </div>
        )}
      </article>

      {/* Bottom navigation */}
      <div className="mx-auto max-w-3xl mt-12 flex items-center justify-between border-t border-gray-200 pt-8">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Volver al inicio
        </Link>

        <Link
          href="/posts/new"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-600 transition-colors hover:text-blue-800"
        >
          Generar nuevo post
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </Link>
      </div>
    </div>
  );
}

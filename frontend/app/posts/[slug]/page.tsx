import { notFound } from 'next/navigation';
import { getAllPosts, getPostBySlug } from '../../lib/api';
import HTMLRenderer from '../../components/HTMLRenderer';
import PostMeta from '../../components/PostMeta';
import Link from 'next/link';

export const dynamic = 'force-static';
export const dynamicParams = false;

interface Props {
  params: Promise<{ slug: string }>;
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
    <article className="py-8">
      <div className="mb-8">
        <Link href="/" className="text-sm font-medium text-accent hover:underline mb-4 inline-block">
          &larr; Volver
        </Link>
        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-4 leading-tight">
          {post.title}
        </h1>
        {post.date && (
          <div className="text-zinc-500 dark:text-zinc-400">
            {new Date(post.date).toLocaleDateString('es-ES', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
        )}
      </div>

      <div className="prose-container">
        <HTMLRenderer htmlContent={post.content} />
      </div>

      <PostMeta metadata={post.metadata} />
    </article>
  );
}

/**
 * Dynamic Post Page
 * 
 * Muestra un post generado por el sistema.
 */

import { notFound } from 'next/navigation';
import fs from 'fs';
import path from 'path';
import BlogLayout from '../../components/BlogLayout';
import PostHeader from '../../components/PostHeader';
import PostBody from '../../components/PostBody';
import type { BlogPost } from '../../types/post';

// Función para obtener posts desde los archivos generados por el backend
async function getPost(slug: string): Promise<BlogPost | null> {
  try {
    const filePath = path.join(process.cwd(), 'public', 'posts', `${slug}.json`);
    
    if (!fs.existsSync(filePath)) {
      return null;
    }

    const fileContents = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(fileContents);
  } catch (error) {
    console.error('Error loading post:', error);
    return null;
  }
}

export default async function PostPage({ 
  params 
}: { 
  params: Promise<{ slug: string }> 
}) {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) {
    notFound();
  }

  return (
    <BlogLayout>
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <PostHeader
          title={post.title}
          description={post.description}
          date={post.metadata.date}
          readingTime={post.metadata.reading_time}
          wordCount={post.metadata.word_count}
          author={post.metadata.author}
          tags={post.metadata.tags}
        />
        
        <PostBody htmlContent={post.html_code} />
        
        {/* Navigation */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <div className="flex justify-between">
            <a
              href="/"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              ← Volver al inicio
            </a>
            <a
              href="/generate"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Generar otro post →
            </a>
          </div>
        </div>
      </article>
    </BlogLayout>
  );
}

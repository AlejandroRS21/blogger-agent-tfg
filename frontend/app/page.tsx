/**
 * Homepage
 * 
 * Página principal del Blogger Agent.
 */

import Link from 'next/link';
import fs from 'fs';
import path from 'path';
import BlogLayout from './components/BlogLayout';
import type { BlogPost } from './types/post';

async function getPosts(): Promise<BlogPost[]> {
  const postsDirectory = path.join(process.cwd(), 'public', 'posts');
  
  if (!fs.existsSync(postsDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(postsDirectory);
  const posts = fileNames
    .filter(fileName => fileName.endsWith('.json'))
    .map(fileName => {
      const filePath = path.join(postsDirectory, fileName);
      const fileContents = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(fileContents);
    });

  return posts.sort((a, b) => new Date(b.metadata.date).getTime() - new Date(a.metadata.date).getTime());
}

export default async function Home() {
  const posts = await getPosts();

  return (
    <BlogLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Blog Header */}
        <section className="text-center mb-16 border-b pb-12">
          <h1 className="text-6xl font-black text-gray-900 mb-4 tracking-tight">
            MI BLOG DE IA
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto font-serif italic">
            "Explorando el futuro, mimetizando el pasado."
          </p>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Posts Area */}
          <div className="lg:col-span-2 space-y-12">
            {posts.length > 0 ? (
              posts.map((post) => (
                <article key={post.id} className="group cursor-pointer">
                  <Link href={`/posts/${post.id}`}>
                    <div className="flex flex-col space-y-3">
                      <div className="flex items-center space-x-2 text-sm text-blue-600 font-bold uppercase tracking-widest">
                        <span>{post.metadata.tags[0] || 'General'}</span>
                        <span>•</span>
                        <span className="text-gray-500">{post.metadata.date}</span>
                      </div>
                      <h2 className="text-3xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {post.title}
                      </h2>
                      <p className="text-gray-600 leading-relaxed line-clamp-3 font-serif line-clamp-3">
                        {post.description}
                      </p>
                      <div className="flex items-center pt-2 text-sm font-semibold text-gray-900">
                        Leer más <span className="ml-1 group-hover:translate-x-1 transition-transform">→</span>
                      </div>
                    </div>
                  </Link>
                </article>
              ))
            ) : (
              <div className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
                <p className="text-gray-500 text-lg">No hay posts publicados todavía.</p>
                <Link href="/generate" className="text-blue-600 font-bold mt-4 inline-block hover:underline">
                  ¡Genera tu primer post desde Daggr!
                </Link>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <aside className="space-y-12">
            <div>
              <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-6 border-b pb-2">
                Sobre el Autor
              </h3>
              <div className="space-y-4">
                <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center text-3xl">
                  🤖
                </div>
                <p className="text-gray-700 font-serif italic">
                  Este es un blog gestionado íntegramente por agentes autónomos de IA que mimetizan estilos de escritura reales.
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-6 border-b pb-2">
                Acciones Rápidas
              </h3>
              <Link href="/generate" className="block w-full text-center bg-gray-900 text-white py-3 px-6 rounded-lg font-bold hover:bg-gray-800 transition">
                Ir al Panel de Generación
              </Link>
            </div>
          </aside>
        </div>
      </div>
    </BlogLayout>
  );
}

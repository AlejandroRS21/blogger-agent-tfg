import { getAllPosts } from './lib/api';
import PostCard from './components/PostCard';
import Link from 'next/link';
import FormattedDate from './components/FormattedDate';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: "BloggerIA | Generación de Contenido con IA",
  description: "Descubre artículos de alta calidad generados por inteligencia artificial que emulan el estilo de los mejores blogueros tecnológicos.",
};

export const dynamic = 'force-static';

export default async function Home() {
  const posts = await getAllPosts();
  const featuredPost = posts[0];
  const remainingPosts = posts.slice(1);

  return (
    <div className="flex flex-col">
      {/* ── Blog Header ── */}
      <section className="border-b border-zinc-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
          <div className="mx-auto max-w-2xl">
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl">
              Blog
            </h1>
            <p className="mt-3 text-base leading-relaxed text-zinc-600">
              Posts generados por el sistema multi-agente de IA. Cada artículo
              está escrito emulando el estilo único de su autor de referencia.
            </p>
          </div>
        </div>
      </section>

      {/* ── Posts Grid ── */}
      <section className="bg-zinc-50 py-12 sm:py-16 min-h-screen">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          {/* Featured post */}
          {featuredPost && (
            <div className="group mb-10">
              <Link
                href={`/posts/${featuredPost.slug}`}
                className="relative block overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm transition-all hover:shadow-lg"
              >
                <div className="grid md:grid-cols-5">
                  <div className="flex flex-col justify-center p-8 md:col-span-3">
                    <span className="mb-3 inline-block w-fit rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                      Destacado
                    </span>
                    <h2 className="text-2xl font-semibold text-zinc-900 transition-colors group-hover:text-blue-600 md:text-3xl">
                      {featuredPost.title}
                    </h2>
                    <p className="mt-3 line-clamp-3 text-sm leading-relaxed text-zinc-600">
                      {featuredPost.excerpt}
                    </p>
                    <div className="mt-5 flex flex-wrap items-center gap-3 text-sm text-zinc-500">
                      <span className="flex items-center gap-1.5">
                        <svg className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                        </svg>
                        <FormattedDate date={featuredPost.date} />
                      </span>
                      <span className="flex items-center gap-1.5">
                        <svg className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        {(featuredPost as any).meta?.reading_time || 5} min
                      </span>
                      <span className="flex items-center gap-1.5">
                        <svg className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {(featuredPost as any).meta?.word_count || 1200} palabras
                      </span>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {featuredPost.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-600"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="hidden items-center justify-center bg-gradient-to-br from-blue-50 to-zinc-50 p-8 md:col-span-2 md:flex">
                    <div className="text-center">
                      <div className="text-6xl">📝</div>
                      <p className="mt-3 text-sm font-medium text-blue-600">
                        Leer post completo →
                      </p>
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          )}

          {/* Remaining posts */}
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {remainingPosts.length > 0 ? (
              remainingPosts.map((post) => (
                <PostCard key={post.slug} post={post} />
              ))
            ) : !featuredPost && (
              <div className="col-span-full py-20 text-center border-2 border-dashed border-zinc-200 rounded-3xl bg-white">
                <p className="text-xl text-zinc-400 italic">
                  Todavía no se ha generado ningún post.
                </p>
              </div>
            )}
          </div>

          {/* Generate CTA */}
          <div className="mt-14 text-center">
            <p className="text-sm text-zinc-500">
              ¿Querés generar tu propio post con el estilo de tu escritor favorito?
            </p>
            <Link
              href="/posts/new"
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
            >
              Generar nuevo post
              <svg className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

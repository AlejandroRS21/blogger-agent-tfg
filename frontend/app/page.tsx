import Link from "next/link";
import PostCard from "@/components/PostCard";
import { getSamplePosts } from "@/lib/api";
import type { BlogPost } from "@/types/post";

const posts = getSamplePosts();
const featuredPost: BlogPost | undefined = posts[0];
const remainingPosts = posts.slice(1, 5);

const steps = [
  {
    number: "01",
    title: "Ingresa tu referencia",
    desc: "Proporciona la URL del blog que quieres emular y el tema sobre el que deseas escribir.",
    color: "bg-blue-500",
  },
  {
    number: "02",
    title: "Analizamos el estilo",
    desc: "El Scraper Agent extrae el contenido y el Style Analyzer captura la voz, el tono y la estructura del autor original.",
    color: "bg-indigo-500",
  },
  {
    number: "03",
    title: "Generamos el contenido",
    desc: "El Writer Agent redacta el post completo en HTML semántico. El Critic Agent lo revisa y mejora.",
    color: "bg-violet-500",
  },
  {
    number: "04",
    title: "Optimizamos y entregamos",
    desc: "El SEO Agent ajusta keywords y meta tags. Recibes el post listo para publicar en tu blog.",
    color: "bg-purple-500",
  },
];

export default function HomePage() {
  return (
    <>
      {/* ── Hero ── */}
      <section className="relative overflow-hidden border-b border-gray-200 bg-gradient-to-b from-white to-gray-50">
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28 lg:py-32">
          <div className="mx-auto max-w-3xl text-center">
            <span className="inline-block rounded-full bg-blue-100 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-blue-700">
              Trabajo de Fin de Grado
            </span>
            <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
              Blogger Agent{" "}
              <span className="text-blue-600">TFG</span>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-gray-600 sm:text-xl">
              Sistema multi-agente de inteligencia artificial que analiza y
              replica estilos de escritura. Genera contenido de blog con la voz
              y el tono de tu escritor favorito.
            </p>
            <div className="mt-10 flex items-center justify-center gap-4">
              <Link
                href="/generate"
                className="rounded-lg bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
              >
                Generar Post Ahora
              </Link>
              <a
                href="https://github.com/AlejandroRS21/blogger-agent-tfg"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
              >
                Ver en GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ── Cómo funciona (workflow paso a paso) ── */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Cómo funciona
            </h2>
            <p className="mt-4 text-gray-600">
              Un pipeline de agentes de IA orquestados que transforman una URL
              y un tema en un post listo para publicar.
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {steps.map((step, i) => (
              <div key={step.number} className="relative">
                {/* Connector line (except last) */}
                {i < steps.length - 1 && (
                  <div className="absolute left-8 top-12 hidden h-[calc(100%+2rem)] w-0.5 bg-gradient-to-b from-blue-200 to-purple-200 lg:block" />
                )}
                <div className="flex items-start gap-4 lg:flex-col lg:items-center lg:text-center">
                  <div
                    className={`flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-2xl text-lg font-bold text-white shadow-md ${step.color}`}
                  >
                    {step.number}
                  </div>
                  <div className="min-w-0 lg:mt-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {step.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-gray-600">
                      {step.desc}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Posts Recientes (blog-style inicio) ── */}
      <section className="border-b border-gray-200 bg-gray-50 py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Posts generados
            </h2>
            <p className="mt-4 text-gray-600">
              Ejemplos del contenido que nuestro sistema es capaz de producir.
            </p>
          </div>

          {/* Featured post */}
          {featuredPost && (
            <div className="group mt-12">
              <Link
                href={`/posts/${featuredPost.slug}`}
                className="relative block overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm transition-all hover:shadow-lg"
              >
                <div className="grid md:grid-cols-5">
                  <div className="flex flex-col justify-center p-8 md:col-span-3">
                    <span className="mb-3 inline-block w-fit rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                      Destacado
                    </span>
                    <h3 className="text-2xl font-bold text-gray-900 transition-colors group-hover:text-blue-600 md:text-3xl">
                      {featuredPost.title}
                    </h3>
                    <p className="mt-3 line-clamp-3 text-sm leading-relaxed text-gray-600">
                      {featuredPost.description}
                    </p>
                    <div className="mt-5 flex flex-wrap items-center gap-3 text-sm text-gray-500">
                      <span className="flex items-center gap-1.5">
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                        </svg>
                        {featuredPost.date}
                      </span>
                      <span className="flex items-center gap-1.5">
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        {featuredPost.reading_time} min
                      </span>
                      <span className="flex items-center gap-1.5">
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {featuredPost.word_count} palabras
                      </span>
                    </div>
                    <div className="mt-5 flex flex-wrap gap-2">
                      {featuredPost.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="hidden items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-50 p-8 md:col-span-2 md:flex">
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

          {/* Remaining posts grid */}
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {remainingPosts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link
              href="/generate"
              className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
            >
              Generar tu propio post
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* ── Tech Stack ── */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Stack Tecnológico
            </h2>
            <p className="mt-4 text-gray-600">
              Tecnologías modernas para un sistema robusto y escalable.
            </p>
          </div>

          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { name: "HuggingFace", description: "Modelos de lenguaje de última generación", icon: "🤗", bg: "bg-yellow-50 border-yellow-200" },
              { name: "Next.js 16", description: "Framework React con App Router y Server Components", icon: "▲", bg: "bg-gray-50 border-gray-200" },
              { name: "Python Backend", description: "Sistema multi-agente asíncrono con Daggr", icon: "🐍", bg: "bg-blue-50 border-blue-200" },
              { name: "Modal", description: "Despliegue serverless en la nube con auto-escalado", icon: "☁️", bg: "bg-green-50 border-green-200" },
            ].map((tech) => (
              <div
                key={tech.name}
                className={`rounded-xl border p-6 text-center ${tech.bg}`}
              >
                <div className="text-3xl">{tech.icon}</div>
                <h3 className="mt-3 font-semibold text-gray-900">{tech.name}</h3>
                <p className="mt-1 text-xs leading-relaxed text-gray-500">
                  {tech.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="bg-gradient-to-b from-gray-50 to-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            ¿Listo para probarlo?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-gray-600">
            Ingresa un tema y el blog de referencia, y deja que los agentes de
            IA hagan el resto.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Link
              href="/generate"
              className="rounded-lg bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
            >
              Generar Post Ahora
            </Link>
            <a
              href="https://huggingface.co/spaces"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
            >
              Explorar en HF Spaces
            </a>
          </div>
        </div>
      </section>
    </>
  );
}

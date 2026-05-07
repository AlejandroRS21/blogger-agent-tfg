import Link from "next/link";
import PostCard from "@/components/PostCard";
import { getSamplePosts } from "@/lib/api";

const features = [
  {
    title: "Analisis Inteligente",
    description:
      "El sistema analiza el estilo de escritura de un blog de referencia usando modelos de lenguaje avanzados de HuggingFace.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
      </svg>
    ),
  },
  {
    title: "Generacion de Contenido",
    description:
      "Crea posts completos en HTML/JSX optimizados para SEO, con titulo, descripcion, palabras clave y estructura semantica.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
      </svg>
    ),
  },
  {
    title: "HTML/JSX Optimizado",
    description:
      "El contenido generado incluye estructura HTML semantica, meta tags, encabezados jerarquicos y formato listo para publicar.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
      </svg>
    ),
  },
];

const techStack = [
  { name: "HuggingFace", description: "Modelos de lenguaje de ultima generacion" },
  { name: "Next.js 16", description: "Framework React con App Router" },
  { name: "Python Backend", description: "Sistema multi-agente asincrono" },
  { name: "Modal", description: "Despliegue serverless en la nube" },
];

export default function HomePage() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-gray-200 bg-gradient-to-b from-white to-gray-50">
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28 lg:py-36">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
              Blogger Agent{" "}
              <span className="text-blue-600">TFG</span>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-gray-600 sm:text-xl">
              Sistema multi-agente de inteligencia artificial capaz de analizar
              y mimetizar estilos de escritura. Genera contenido de blog con la
              voz y el tono de tu escritor favorito.
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

      {/* Features */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Como funciona
            </h2>
            <p className="mt-4 text-gray-600">
              El sistema utiliza un pipeline de agentes especializados para
              generar contenido de alta calidad.
            </p>
          </div>

          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="group rounded-xl border border-gray-200 bg-white p-8 transition-shadow hover:shadow-md"
              >
                <div className="mb-4 inline-flex rounded-lg bg-blue-50 p-3 text-blue-600">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sample Posts */}
      <section className="border-b border-gray-200 bg-gray-50 py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Posts Recientes
            </h2>
            <p className="mt-4 text-gray-600">
              Ejemplos del contenido generado por nuestro sistema multi-agente.
            </p>
          </div>

          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {getSamplePosts().slice(0, 6).map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>

          <div className="mt-10 text-center">
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

      {/* Tech Stack */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Stack Tecnologico
            </h2>
            <p className="mt-4 text-gray-600">
              Tecnologias modernas para un sistema robusto y escalable.
            </p>
          </div>

          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {techStack.map((tech) => (
              <div
                key={tech.name}
                className="rounded-lg border border-gray-200 bg-white p-6 text-center"
              >
                <h3 className="font-semibold text-gray-900">{tech.name}</h3>
                <p className="mt-1 text-xs text-gray-500">
                  {tech.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Daggr / HuggingFace Workflow */}
      <section className="border-b border-gray-200 bg-gray-50 py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Pipeline Multi-Agente con <span className="text-yellow-600">Daggr</span>
            </h2>
            <p className="mt-4 text-gray-600">
              El sistema orquesta agentes especializados en un pipeline secuencial
              impulsado por modelos de HuggingFace.
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {[
              {
                step: "1",
                title: "Scraper Agent",
                desc: "Extrae y analiza el contenido del blog de referencia para capturar el estilo y tono del escritor.",
              },
              {
                step: "2",
                title: "Writer Agent",
                desc: "Genera el post completo en HTML semántico respetando la voz del autor original.",
              },
              {
                step: "3",
                title: "Critic Agent",
                desc: "Revisa y mejora el contenido evaluando calidad, coherencia y estructura.",
              },
              {
                step: "4",
                title: "SEO Agent",
                desc: "Optimiza keywords, meta tags y estructura para posicionamiento en buscadores.",
              },
            ].map((agent) => (
              <div
                key={agent.step}
                className="relative rounded-xl border border-gray-200 bg-white p-6 text-center shadow-sm"
              >
                <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-yellow-100 text-sm font-bold text-yellow-700">
                  {agent.step}
                </div>
                <h3 className="font-semibold text-gray-900">{agent.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">
                  {agent.desc}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-12 rounded-xl border border-yellow-200 bg-yellow-50 p-6 sm:p-8">
            <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
              <div className="flex-shrink-0 text-3xl">🤗</div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">
                  Impulsado por HuggingFace
                </h3>
                <p className="mt-1 text-sm text-gray-600">
                  Todos los agentes utilizan modelos open-source de HuggingFace
                  desplegados en Modal. El pipeline completo está disponible como
                  HuggingFace Space para ejecución interactiva.
                </p>
              </div>
              <a
                href="https://huggingface.co/spaces"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-shrink-0 rounded-lg bg-yellow-400 px-6 py-3 text-sm font-semibold text-gray-900 shadow-sm transition-colors hover:bg-yellow-500"
              >
                Explorar en HF Spaces
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Listo para probarlo?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-gray-600">
            Ingresa un tema y el blog de referencia, y deja que los agentes de
            IA hagan el resto.
          </p>
          <div className="mt-8">
            <Link
              href="/generate"
              className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
            >
              Generar Post Ahora
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

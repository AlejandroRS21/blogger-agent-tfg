import Link from "next/link";

export const metadata = {
  title: "Sobre el proyecto",
};

const timeline = [
  {
    year: "2024",
    title: "Idea inicial",
    desc: "Nace la idea de un sistema multi-agente que pueda analizar y replicar estilos de escritura usando modelos open-source de HuggingFace.",
  },
  {
    year: "2025",
    title: "Arquitectura y desarrollo",
    desc: "Se define la arquitectura de agentes (Scraper, Writer, Critic, SEO) y se construye el pipeline. Se integra con Modal para despliegue serverless y Supabase para persistencia.",
  },
  {
    year: "2026",
    title: "Versión actual",
    desc: "El sistema está operativo, generando posts reales. Este blog es el frontend que muestra los resultados del proyecto.",
  },
];

export default function AboutPage() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-gray-200 bg-gradient-to-b from-white to-gray-50">
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28">
          <div className="mx-auto max-w-3xl text-center">
            <span className="inline-block rounded-full bg-blue-100 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-blue-700">
              Sobre el proyecto
            </span>
            <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
              Blog generado por{" "}
              <span className="text-blue-600">inteligencia artificial</span>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-gray-600 sm:text-xl">
              Cada post que ves acá fue escrito por un sistema multi-agente de IA
              que analiza el estilo de escritura de un autor y genera contenido
              nuevo con su voz.
            </p>
          </div>
        </div>
      </section>

      {/* Qué es */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-3xl">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900">
              ¿Qué es esto?
            </h2>
            <p className="mt-6 text-base leading-relaxed text-gray-600">
              <strong>Blogger Agent TFG</strong> es un Trabajo de Fin de Grado
              que explora cómo los modelos de lenguaje open-source pueden
              mimetizar estilos de escritura humanos.
            </p>
            <p className="mt-4 text-base leading-relaxed text-gray-600">
              El sistema funciona con un pipeline de agentes de IA:
            </p>
            <ul className="mt-4 list-inside list-disc space-y-2 text-base leading-relaxed text-gray-600">
              <li>
                <strong className="text-gray-900">Scraper Agent</strong> —
                extrae contenido de un blog de referencia
              </li>
              <li>
                <strong className="text-gray-900">Writer Agent</strong> —
                genera el post imitando el estilo analizado
              </li>
              <li>
                <strong className="text-gray-900">Critic Agent</strong> —
                revisa y mejora la calidad del contenido
              </li>
              <li>
                <strong className="text-gray-900">SEO Agent</strong> —
                optimiza keywords, meta tags y estructura
              </li>
            </ul>
            <p className="mt-4 text-base leading-relaxed text-gray-600">
              Todo corre sobre modelos open-source de{" "}
              <a
                href="https://huggingface.co"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-blue-600 underline decoration-blue-200 underline-offset-2 hover:text-blue-800"
              >
                HuggingFace
              </a>{" "}
              desplegados en{" "}
              <a
                href="https://modal.com"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-blue-600 underline decoration-blue-200 underline-offset-2 hover:text-blue-800"
              >
                Modal
              </a>
              .
            </p>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="border-b border-gray-200 bg-gray-50 py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-3xl">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900">
              Historia del proyecto
            </h2>

            <div className="relative mt-12">
              {/* Vertical line */}
              <div className="absolute left-4 top-0 h-full w-0.5 bg-gradient-to-b from-blue-200 via-indigo-200 to-purple-200" />

              {timeline.map((item, i) => (
                <div key={item.year} className="relative ml-12 pb-12 last:pb-0">
                  {/* Dot */}
                  <div className="absolute -left-[3.25rem] mt-1 flex h-6 w-6 items-center justify-center rounded-full border-4 border-white bg-blue-500 shadow">
                    <span className="text-[10px] font-bold text-white">
                      {i + 1}
                    </span>
                  </div>
                  <div>
                    <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                      {item.year}
                    </span>
                    <h3 className="mt-2 text-xl font-bold text-gray-900">
                      {item.title}
                    </h3>
                    <p className="mt-2 text-base leading-relaxed text-gray-600">
                      {item.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Stack */}
      <section className="border-b border-gray-200 bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-3xl">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900">
              Stack tecnológico
            </h2>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {[
                {
                  label: "Frontend",
                  tech: "Next.js 16, Tailwind CSS, TypeScript",
                },
                {
                  label: "Backend",
                  tech: "Python, FastAPI, Daggr (workflow)",
                },
                {
                  label: "Modelos",
                  tech: "HuggingFace, Llama / Mistral / Qwen",
                },
                { label: "Infra", tech: "Modal (serverless), Supabase (DB)" },
              ].map((item) => (
                <div
                  key={item.label}
                  className="rounded-xl border border-gray-200 bg-gray-50 p-5"
                >
                  <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    {item.label}
                  </p>
                  <p className="mt-1 font-medium text-gray-900">{item.tech}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            ¿Querés generar tu propio post?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-gray-600">
                Elegí un tema y un blog de referencia, y deja que los agentes hagan
            el resto.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <Link
              href="/posts/new"
              className="rounded-lg bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
            >
              Generar Post Ahora
            </Link>
            <Link
              href="/project"
              className="rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
            >
              Ver el proyecto técnico
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

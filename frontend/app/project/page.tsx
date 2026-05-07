import Link from "next/link";

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

export default function ProjectPage() {
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

      {/* ── Cómo funciona ── */}
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

          {/* Detalle de agentes */}
          <div className="mt-20">
            <h3 className="text-center text-2xl font-bold text-gray-900">
              Agentes del pipeline
            </h3>
            <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-600">
              Cada agente tiene una responsabilidad específica dentro del flujo de trabajo.
            </p>

            <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[
                {
                  title: "Scraper Agent",
                  desc: "Extrae y analiza el contenido del blog de referencia usando técnicas de web scraping avanzado.",
                  icon: "🕷️",
                },
                {
                  title: "Writer Agent",
                  desc: "Genera el post completo en HTML semántico respetando la voz, el tono y la estructura del autor original.",
                  icon: "✍️",
                },
                {
                  title: "Critic Agent",
                  desc: "Evalúa la calidad, coherencia y precisión del contenido generado, sugiriendo mejoras.",
                  icon: "🔍",
                },
                {
                  title: "SEO Agent",
                  desc: "Optimiza palabras clave, meta tags, encabezados y estructura para posicionamiento en buscadores.",
                  icon: "📈",
                },
              ].map((agent) => (
                <div
                  key={agent.title}
                  className="rounded-xl border border-gray-200 bg-gray-50 p-6 text-center"
                >
                  <div className="text-4xl">{agent.icon}</div>
                  <h4 className="mt-4 font-semibold text-gray-900">{agent.title}</h4>
                  <p className="mt-2 text-sm leading-relaxed text-gray-600">
                    {agent.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* HuggingFace callout */}
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

      {/* ── Stack Tecnológico ── */}
      <section className="border-b border-gray-200 bg-gray-50 py-20 sm:py-28">
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
              { name: "Next.js 16", description: "Framework React con App Router y Server Components", icon: "▲", bg: "bg-white border-gray-200" },
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
      <section className="bg-white py-20 sm:py-28">
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
              href="https://github.com/AlejandroRS21/blogger-agent-tfg"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
            >
              Ver en GitHub
            </a>
          </div>
        </div>
      </section>
    </>
  );
}

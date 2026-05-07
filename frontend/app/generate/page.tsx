import GenerateForm from "@/components/GenerateForm";

const workflowSteps = [
  {
    number: 1,
    title: "Analisis del blog de referencia",
    description: "El sistema analiza el estilo, tono y estructura del blog proporcionado.",
  },
  {
    number: 2,
    title: "Interpretacion del tema",
    description: "Los agentes de IA procesan el tema y las palabras clave para entender el contexto.",
  },
  {
    number: 3,
    title: "Generacion de estructura",
    description: "Se crea un esquema del articulo con secciones y puntos clave.",
  },
  {
    number: 4,
    title: "Redaccion del contenido",
    description: "El modelo genera el contenido completo mimetizando el estilo del blog de referencia.",
  },
  {
    number: 5,
    title: "Optimizacion HTML/JSX",
    description: "El contenido se convierte a HTML semantico con meta tags y estructura SEO.",
  },
  {
    number: 6,
    title: "Calculo de metricas",
    description: "Se calculan palabras, tiempo de lectura y se extraen encabezados.",
  },
  {
    number: 7,
    title: "Entrega del resultado",
    description: "El post generado se presenta listo para revisar y publicar.",
  },
];

export default function GeneratePage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
      <div className="grid gap-12 lg:grid-cols-5">
        {/* Form section */}
        <div className="lg:col-span-3">
          <div className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">
              Generar Post
            </h1>
            <p className="mt-2 text-gray-600">
              Completa los campos y deja que los agentes de IA generen un post
              con el estilo del blog de referencia.
            </p>
          </div>

          <GenerateForm />
        </div>

        {/* Workflow info */}
        <div className="lg:col-span-2">
          <div className="sticky top-24">
            <h2 className="text-lg font-semibold text-gray-900">
              Proceso de generacion
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              El sistema sigue un pipeline de 7 fases:
            </p>

            <div className="mt-6 space-y-4">
              {workflowSteps.map((step) => (
                <div key={step.number} className="flex gap-3">
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">
                    {step.number}
                  </span>
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">
                      {step.title}
                    </h3>
                    <p className="mt-0.5 text-xs text-gray-500">
                      {step.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-lg border border-blue-200 bg-blue-50 p-4">
              <h3 className="text-sm font-semibold text-blue-800">
                Modo de desarrollo
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-blue-700">
                Actualmente el sistema opera en modo simulado. Los posts se generan
                con datos de ejemplo para probar la interfaz. En produccion, se
                conectara al backend real en Modal.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

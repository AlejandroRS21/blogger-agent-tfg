"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const PHASES = [
  { id: "safety", label: "Protección de Contenido", icon: "🛡️", duration: 5000 },
  { id: "style", label: "Análisis de Estilo", icon: "🕵️", duration: 8000 },
  { id: "keywords", label: "Extracción de Keywords", icon: "🔑", duration: 4000 },
  { id: "generation", label: "Generación de Contenido", icon: "📝", duration: 25000 },
  { id: "critique", label: "Refinamiento y Crítica", icon: "🧐", duration: 15000 },
  { id: "images", label: "Selección de Imágenes", icon: "🖼️", duration: 7000 },
  { id: "publishing", label: "Publicación en GitHub", icon: "🚀", duration: 6000 },
];

export default function NewPostPage() {
  const [topic, setTopic] = useState("");
  const [urls, setUrls] = useState("https://javipas.com");
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isGenerating && currentPhase < PHASES.length) {
      const phase = PHASES[currentPhase];
      const stepProgress = 100 / PHASES.length;
      
      timer = setTimeout(() => {
        setCurrentPhase((prev) => prev + 1);
        setProgress((prev) => Math.min(prev + stepProgress, 100));
      }, phase.duration);
    }
    return () => clearTimeout(timer);
  }, [isGenerating, currentPhase]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setCurrentPhase(0);
    setProgress(0);
    setError(null);

    try {
      const webhookUrl = process.env.NEXT_PUBLIC_MODAL_WEBHOOK_URL || "https://alejandrors21--blogger-agent-tfg-webhook.modal.run";
      
      const response = await fetch(webhookUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic,
          blogger_urls: urls.split(",").map(u => u.trim()),
          provider: "huggingface"
        }),
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error || "Error desconocido en la generación");
      }

      // If successful, wait a bit for the last phase animation and redirect
      setTimeout(() => {
        router.push("/");
        router.refresh();
      }, 2000);

    } catch (err: any) {
      setError(err.message);
      setIsGenerating(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto px-6 py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4">Crear Nuevo Post</h1>
        <p className="text-secondary text-lg">
          Configura el tema y la fuente de inspiración para que la IA haga su magia.
        </p>
      </div>

      {!isGenerating ? (
        <form onSubmit={handleSubmit} className="space-y-8 bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="space-y-2">
            <label htmlFor="topic" className="block text-sm font-semibold uppercase tracking-wider">
              Tema del Post
            </label>
            <input
              id="topic"
              type="text"
              required
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Ej: El futuro de la IA en el desarrollo web"
              className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-accent outline-none transition-all"
            />
            <p className="text-xs text-secondary italic">El Agente Guardián validará que el tema sea profesional.</p>
          </div>

          <div className="space-y-2">
            <label htmlFor="urls" className="block text-sm font-semibold uppercase tracking-wider">
              URLs de Inspiración (Separadas por coma)
            </label>
            <input
              id="urls"
              type="text"
              required
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-accent outline-none transition-all"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-primary text-background font-bold py-4 rounded-xl hover:opacity-90 transition-opacity active:scale-[0.98] transform"
          >
            GENERAR POST AUTÓNOMO
          </button>
          
          {error && (
            <div className="p-4 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-xl border border-red-100 dark:border-red-800 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}
        </form>
      ) : (
        <div className="space-y-12 py-12">
          {/* Progress Section */}
          <div className="relative pt-1">
            <div className="flex mb-4 items-center justify-between">
              <div>
                <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-accent bg-accent/10">
                  Progreso de Generación
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block text-accent">
                  {Math.round(progress)}%
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-3 mb-4 text-xs flex rounded-full bg-slate-100 dark:bg-slate-800">
              <div
                style={{ width: `${progress}%` }}
                className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-accent transition-all duration-1000 ease-out"
              ></div>
            </div>
          </div>

          {/* Phases List */}
          <div className="grid gap-4">
            {PHASES.map((phase, index) => (
              <div 
                key={phase.id}
                className={`flex items-center p-4 rounded-xl border transition-all duration-500 ${
                  index === currentPhase 
                    ? "bg-accent/5 border-accent scale-[1.02] shadow-md" 
                    : index < currentPhase 
                    ? "bg-slate-50 dark:bg-slate-800/50 border-transparent opacity-60" 
                    : "bg-transparent border-slate-200 dark:border-slate-800 opacity-40"
                }`}
              >
                <span className="text-2xl mr-4">{phase.icon}</span>
                <div className="flex-1">
                  <h3 className={`font-bold ${index === currentPhase ? "text-accent" : ""}`}>
                    {phase.label}
                  </h3>
                  <p className="text-xs text-secondary">
                    {index === currentPhase ? "En proceso..." : index < currentPhase ? "Completado" : "Pendiente"}
                  </p>
                </div>
                {index === currentPhase && (
                  <div className="w-2 h-2 bg-accent rounded-full animate-ping"></div>
                )}
                {index < currentPhase && (
                  <span className="text-green-500 text-xl">✓</span>
                )}
              </div>
            ))}
          </div>

          <p className="text-center text-secondary italic animate-pulse">
            Por favor, no cierres esta ventana. El proceso toma unos 2-3 minutos.
          </p>
        </div>
      )}
    </main>
  );
}

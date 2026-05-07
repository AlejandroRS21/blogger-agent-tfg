"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { generatePost } from "@/lib/api";
import type { GenerateResponse } from "@/types/post";

export default function GenerateForm() {
  const router = useRouter();
  const [topic, setTopic] = useState("");
  const [blogUrl, setBlogUrl] = useState("https://javipas.com");
  const [keywords, setKeywords] = useState("");
  const [provider, setProvider] = useState<"huggingface" | "openai" | "gemini">("huggingface");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GenerateResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!topic.trim()) {
      setError("El tema es obligatorio");
      return;
    }

    if (!blogUrl.trim()) {
      setError("La URL del blog es obligatoria");
      return;
    }

    setLoading(true);

    try {
      const keywordsArray = keywords
        .split(",")
        .map((k) => k.trim())
        .filter(Boolean);

      const response = await generatePost({
        topic: topic.trim(),
        blog_url: blogUrl.trim(),
        keywords: keywordsArray.length > 0 ? keywordsArray : undefined,
        provider,
      });

      if (response.success && response.post) {
        setResult(response);
      } else {
        setError(response.error || "Error al generar el post");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado");
    } finally {
      setLoading(false);
    }
  };

  const handleViewPost = () => {
    if (result?.post?.slug) {
      router.push(`/posts/${result.post.slug}`);
    }
  };

  if (result?.post) {
    return (
      <div className="space-y-6">
        <div className="rounded-lg border border-green-200 bg-green-50 p-6">
          <div className="flex items-center gap-2">
            <svg className="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="font-semibold text-green-800">
              Post generado exitosamente
            </h3>
          </div>
          {result.execution_time && (
            <p className="mt-1 text-sm text-green-600">
              Tiempo de ejecucion: {result.execution_time}s
            </p>
          )}
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900">
            {result.post.title}
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            {result.post.description}
          </p>

          <div className="mt-4 flex items-center gap-4 text-xs text-gray-500">
            <span>{result.post.date}</span>
            <span>{result.post.reading_time} min lectura</span>
            <span>{result.post.word_count} palabras</span>
          </div>

          {result.post.tags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {result.post.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleViewPost}
            className="rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700"
          >
            Ver post completo
          </button>
          <button
            onClick={() => {
              setResult(null);
              setTopic("");
              setKeywords("");
            }}
            className="rounded-lg border border-gray-300 bg-white px-6 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            Generar otro
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Topic */}
      <div>
        <label
          htmlFor="topic"
          className="block text-sm font-medium text-gray-900"
        >
          Tema del post <span className="text-red-500">*</span>
        </label>
        <textarea
          id="topic"
          rows={3}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Ej: Inteligencia Artificial en la educacion, Blockchain para supply chain..."
          className="mt-1.5 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 placeholder-gray-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          required
        />
      </div>

      {/* Blog URL */}
      <div>
        <label
          htmlFor="blogUrl"
          className="block text-sm font-medium text-gray-900"
        >
          URL del blog de referencia <span className="text-red-500">*</span>
        </label>
        <input
          id="blogUrl"
          type="url"
          value={blogUrl}
          onChange={(e) => setBlogUrl(e.target.value)}
          placeholder="https://javipas.com"
          className="mt-1.5 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 placeholder-gray-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          required
        />
        <p className="mt-1 text-xs text-gray-500">
          El sistema analizara el estilo de escritura de este blog
        </p>
      </div>

      {/* Keywords */}
      <div>
        <label
          htmlFor="keywords"
          className="block text-sm font-medium text-gray-900"
        >
          Palabras clave (opcional)
        </label>
        <input
          id="keywords"
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="IA, machine learning, tutorial"
          className="mt-1.5 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 placeholder-gray-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        />
        <p className="mt-1 text-xs text-gray-500">
          Separa con comas. El modelo las usara como referencia.
        </p>
      </div>

      {/* Provider */}
      <div>
        <label
          htmlFor="provider"
          className="block text-sm font-medium text-gray-900"
        >
          Proveedor de IA
        </label>
        <select
          id="provider"
          value={provider}
          onChange={(e) => setProvider(e.target.value as typeof provider)}
          className="mt-1.5 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        >
          <option value="huggingface">HuggingFace</option>
          <option value="openai">OpenAI</option>
          <option value="gemini">Gemini</option>
        </select>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <div className="flex items-start gap-2">
            <svg className="mt-0.5 h-4 w-4 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? (
          <>
            <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
            Generando post...
          </>
        ) : (
          "Generar Post"
        )}
      </button>
    </form>
  );
}

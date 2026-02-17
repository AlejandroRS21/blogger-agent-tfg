/**
 * GenerateForm Component
 * 
 * Formulario para generar un nuevo blog post usando el backend.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import type { GenerateRequest, GenerateResponse } from '../types/post';

export default function GenerateForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    blogger_name: '',
    blogger_bio: '',
    blogger_sample_posts: [''],
    topic: '',
    keywords: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const requestData: GenerateRequest = {
        blogger_name: formData.blogger_name,
        blogger_bio: formData.blogger_bio,
        blogger_sample_posts: formData.blogger_sample_posts.filter(Boolean),
        topic: formData.topic,
        keywords: formData.keywords.split(',').map(k => k.trim()).filter(Boolean)
      };

      const response = await fetch('/api/generate-post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      const data: GenerateResponse = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Error al generar el post');
      }

      // Redirect to the generated post
      if (data.post) {
        router.push(`/posts/${data.post.id}`);
      } else {
        throw new Error('No se recibió el post generado');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsLoading(false);
    }
  };

  const addSamplePost = () => {
    setFormData({
      ...formData,
      blogger_sample_posts: [...formData.blogger_sample_posts, '']
    });
  };

  const removeSamplePost = (index: number) => {
    setFormData({
      ...formData,
      blogger_sample_posts: formData.blogger_sample_posts.filter((_, i) => i !== index)
    });
  };

  const updateSamplePost = (index: number, value: string) => {
    const updated = [...formData.blogger_sample_posts];
    updated[index] = value;
    setFormData({ ...formData, blogger_sample_posts: updated });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md">
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 font-medium">Error:</p>
          <p className="text-red-500 text-sm mt-1">{error}</p>
        </div>
      )}
      
      <div className="space-y-6">
        {/* Blogger Name */}
        <div>
          <label htmlFor="blogger_name" className="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Blogger *
          </label>
          <input
            type="text"
            id="blogger_name"
            value={formData.blogger_name}
            onChange={(e) => setFormData({ ...formData, blogger_name: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ej: Javier Pastor"
            required
          />
        </div>

        {/* Blogger Bio */}
        <div>
          <label htmlFor="blogger_bio" className="block text-sm font-medium text-gray-700 mb-2">
            Biografía del Blogger *
          </label>
          <textarea
            id="blogger_bio"
            value={formData.blogger_bio}
            onChange={(e) => setFormData({ ...formData, blogger_bio: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ej: Periodista tecnológico con más de 20 años de experiencia..."
            rows={3}
            required
          />
        </div>

        {/* Sample Posts */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Posts de Ejemplo (URLs) *
          </label>
          {formData.blogger_sample_posts.map((post, index) => (
            <div key={index} className="flex gap-2 mb-2">
              <input
                type="url"
                value={post}
                onChange={(e) => updateSamplePost(index, e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="https://ejemplo.com/post"
                required
              />
              {formData.blogger_sample_posts.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeSamplePost(index)}
                  className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg"
                >
                  ✕
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={addSamplePost}
            className="mt-2 text-sm text-blue-600 hover:text-blue-700"
          >
            + Agregar otro post
          </button>
          <p className="mt-1 text-xs text-gray-500">
            El sistema analizará estos posts para capturar el estilo del blogger
          </p>
        </div>

        {/* Topic */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            Tema del Post *
          </label>
          <input
            type="text"
            id="topic"
            value={formData.topic}
            onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ej: Las mejores prácticas para desarrollo con IA"
            required
          />
        </div>

        {/* Keywords */}
        <div>
          <label htmlFor="keywords" className="block text-sm font-medium text-gray-700 mb-2">
            Palabras Clave (opcional)
          </label>
          <input
            type="text"
            id="keywords"
            value={formData.keywords}
            onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="IA, machine learning, desarrollo (separadas por comas)"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generando post...
            </span>
          ) : (
            'Generar Post'
          )}
        </button>
      </div>

      {isLoading && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-blue-700 text-sm">
            ⏳ El sistema está analizando el estilo, generando contenido y creando el HTML/JSX...
            <br />
            Esto puede tomar 1-2 minutos.
          </p>
        </div>
      )}
    </form>
  );
}

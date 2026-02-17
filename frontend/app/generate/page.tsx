/**
 * Generate Post Page
 * 
 * Página con el formulario para generar posts con el Blogger Agent.
 */

import BlogLayout from '../components/BlogLayout';
import GenerateForm from '../components/GenerateForm';

export default function GeneratePage() {
  return (
    <BlogLayout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Generar Nuevo Post
          </h1>
          <p className="text-lg text-gray-600">
            Proporciona los datos del blogger y un tema, la IA generará contenido en su estilo
          </p>
        </div>

        <GenerateForm />

        <div className="mt-8 bg-blue-50 p-6 rounded-lg">
          <h2 className="text-lg font-semibold mb-2">ℹ️ ¿Cómo funciona?</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li><strong>Análisis de Estilo:</strong> Extrae el tono, voz y estructura del blogger</li>
            <li><strong>Extracción de Keywords:</strong> Identifica palabras clave del tema</li>
            <li><strong>Generación de Contenido:</strong> Crea el artículo con IA (HuggingFace)</li>
            <li><strong>Revisión Crítica:</strong> Valida autenticidad y coherencia</li>
            <li><strong>Selección de Imágenes:</strong> Elige imágenes relevantes</li>
            <li><strong>HTML Builder:</strong> Genera código limpio y optimizado</li>
          </ol>
        </div>
      </div>
    </BlogLayout>
  );
}

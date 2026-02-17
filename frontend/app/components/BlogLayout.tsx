/**
 * BlogLayout Component
 * 
 * Layout principal para las páginas del blog.
 * Incluye header, footer y  estructura general.
 */

import Link from 'next/link';
import { ReactNode } from 'react';

interface BlogLayoutProps {
  children: ReactNode;
  className?: string;
}

export default function BlogLayout({ children, className = '' }: BlogLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-gray-900 hover:text-blue-600 transition">
              Blogger Agent
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-gray-600 hover:text-gray-900 transition">
                Inicio
              </Link>
              <Link href="/generate" className="text-gray-600 hover:text-gray-900 transition">
                Generar Post
              </Link>
            </div>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className={`flex-grow ${className}`}>
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} Blogger Agent TFG - Sistema Multi-Agente para Generación de Contenido
          </p>
          <p className="text-center text-gray-400 text-xs mt-2">
            Powered by HuggingFace 🤗 | Next.js | Modal
          </p>
        </div>
      </footer>
    </div>
  );
}

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from 'next/link';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "BloggerIA | Sistema Multi-Agente de Generación Editorial",
    template: "%s | BloggerIA"
  },
  description: "Un sistema avanzado de orquestación de IA diseñado para generar contenido editorial de alta calidad, mimetizando estilos de escritura.",
  metadataBase: new URL('https://javipas-agent.vercel.app'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "BloggerIA",
    description: "Sistema Multi-Agente de Generación Editorial",
    url: 'https://javipas-agent.vercel.app',
    siteName: 'BloggerIA',
    locale: 'es_ES',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "BloggerIA",
    description: "Sistema Multi-Agente de Generación Editorial",
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="scroll-smooth">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-white text-stone-900 dark:bg-stone-950 dark:text-stone-100 min-h-screen flex flex-col`}
      >
        <header className="sticky top-0 z-50 border-b border-gray-200/80 bg-white/95 backdrop-blur-md supports-[backdrop-filter]:bg-white/80">
          <nav className="container mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
            <Link href="/" className="group flex items-center gap-2">
              <span className="text-2xl font-extrabold tracking-tight text-gray-900 transition-colors group-hover:text-blue-600">
                BLOGGER<span className="text-blue-600">IA</span>
              </span>
            </Link>

            <nav className="flex items-center gap-6">
              <Link href="/" className="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600">Blog</Link>
              <Link href="/project" className="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600">Proyecto</Link>
              <Link href="/posts/new" className="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600">Generar</Link>
              <a href="https://javipas.com" target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-gray-500 transition-colors hover:text-blue-600">Original</a>
              <a href="https://github.com/AlejandroRS21/blogger-agent-tfg" target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-gray-500 transition-colors hover:text-blue-600">GitHub</a>
              <a href="https://huggingface.co/spaces/AlejandroRS21/blogger-agent-tfg" target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 text-sm font-medium text-gray-500 transition-colors hover:text-blue-600">
                <span>🤗</span><span className="hidden sm:inline">HF Spaces</span>
              </a>
            </nav>
          </nav>
        </header>

        <main className="flex-grow">
          {children}
        </main>

        <footer className="border-t border-stone-200 dark:border-stone-800 py-12 mt-20">
          <div className="container mx-auto px-4 text-center text-stone-500 dark:text-stone-400 text-sm">
            <p className="font-mono mb-4">© 2026 BloggerIA - Generado con IA & Aphra</p>
            <div className="flex justify-center gap-4">
              <span>Next.js 16</span>
              <span>•</span>
              <span>Tailwind CSS v4</span>
              <span>•</span>
              <span>Static Export</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}

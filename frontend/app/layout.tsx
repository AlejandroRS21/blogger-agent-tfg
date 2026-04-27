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
    default: "Blog Javi Pas | Tecnología, Cacharreo y Opinión",
    template: "%s | Blog Javi Pas"
  },
  description: "El blog personal de Javi Pas. Analizamos la tecnología con alma, humor y espíritu crítico. IA, dispositivos y experimentos desde el miniresort.",
  metadataBase: new URL('https://javipas-agent.vercel.app'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Blog Javi Pas",
    description: "Tecnología, Cacharreo y Opinión con un toque personal.",
    url: 'https://javipas-agent.vercel.app',
    siteName: 'Blog Javi Pas',
    locale: 'es_ES',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "Blog Javi Pas",
    description: "Tecnología y Cacharreo con alma.",
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
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-stone-50 text-stone-900 dark:bg-stone-950 dark:text-stone-100 min-h-screen flex flex-col`}
      >
        <header className="sticky top-0 z-50 w-full border-b border-stone-200 bg-white/80 backdrop-blur-md dark:border-stone-800 dark:bg-stone-950/80">
          <nav className="container mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="text-xl font-black tracking-tighter hover:opacity-80 transition-opacity">
              JAVI <span className="text-red-600">PAS</span>
            </Link>
            <div className="flex gap-6 text-sm font-medium uppercase tracking-widest">
              <Link href="/" className="hover:text-red-600 transition-colors">Inicio</Link>
              <a href="https://javipas.com" target="_blank" rel="noopener noreferrer" className="hover:text-red-600 transition-colors">Original</a>
            </div>
          </nav>
        </header>

        <main className="flex-grow container mx-auto px-4 max-w-5xl">
          {children}
        </main>

        <footer className="border-t border-stone-200 dark:border-stone-800 py-12 mt-20">
          <div className="container mx-auto px-4 text-center text-stone-500 dark:text-stone-400 text-sm">
            <p className="font-mono mb-4">© 2026 Blog Javi Pas - Generado con IA & Aphra</p>
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

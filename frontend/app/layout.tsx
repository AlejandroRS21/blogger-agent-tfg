import type { Metadata } from "next";
import "./globals.css";
import Link from 'next/link';

export const metadata: Metadata = {
  title: "Mock Javipas - AI Generated",
  description: "Un blog simulado con IA.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="antialiased">
      <body className="min-h-screen bg-background text-foreground selection:bg-accent/10">
        <div className="max-w-3xl mx-auto px-6 sm:px-8 flex flex-col min-h-screen">
          
          <header className="py-10 md:py-14 border-b border-zinc-100 dark:border-zinc-900 mb-8">
            <nav className="flex items-center justify-between">
              <Link href="/" className="group flex items-center gap-1">
                <span className="font-black text-3xl tracking-tighter text-accent group-hover:scale-105 transition-transform">
                  AI
                </span>
                <span className="font-bold text-2xl tracking-tight text-primary">
                  Blogger
                </span>
              </Link>
              <div className="hidden sm:block text-xs font-semibold tracking-widest uppercase text-secondary">
                Autonomous Content Lab
              </div>
            </nav>
          </header>

          <main className="flex-1">
            {children}
          </main>

          <footer className="py-12 mt-20 border-t border-zinc-100 dark:border-zinc-900 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs font-medium text-secondary">
            <div className="flex items-center gap-4">
              <span>© {new Date().getFullYear()} AI Blogger.</span>
              <span className="h-4 w-px bg-zinc-200 dark:bg-zinc-800" />
              <span>Estilo inspirado en Javipas</span>
            </div>
            <div className="flex items-center gap-6">
              <a href="#" className="hover:text-accent">Twitter</a>
              <a href="#" className="hover:text-accent">GitHub</a>
              <a href="#" className="hover:text-accent">RSS</a>
            </div>
          </footer>

        </div>
      </body>
    </html>
  );
}

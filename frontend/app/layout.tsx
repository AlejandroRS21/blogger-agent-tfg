import type { Metadata } from "next";
import "./globals.css";
import Link from 'next/link';

/**
 * Global Metadata Configuration for SEO
 * Following the style and keywords of javipas.com
 */
export const metadata: Metadata = {
  title: {
    default: "AI Blogger | Tecnología, IA y Reflexiones",
    template: "%s | AI Blogger"
  },
  description: "Un blog de tecnología y reflexiones generadas por inteligencia artificial, inspirado en el estilo de Javipas.",
  keywords: ["IA", "Inteligencia Artificial", "Tecnología", "Gadgets", "Reflexiones", "Blogger Agent", "Javipas"],
  authors: [{ name: "Blogger Agent" }],
  creator: "Blogger Agent",
  publisher: "Blogger Agent",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://ai-blogger.vercel.app"), // Replace with actual URL when known
  openGraph: {
    title: "AI Blogger | Tecnología, IA y Reflexiones",
    description: "Contenido generado por IA con estilo personal.",
    url: "https://ai-blogger.vercel.app",
    siteName: "AI Blogger",
    locale: "es_ES",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Blogger | Tecnología, IA y Reflexiones",
    description: "Contenido generado por IA con estilo personal.",
    creator: "@AIBlogger",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/icon.png', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-icon.png' },
    ],
  },
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
                <span className="font-bold text-2xl tracking-tight text-primary hover:no-underline">
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
              <a href="https://twitter.com/javipas" target="_blank" rel="noopener noreferrer" className="hover:text-accent">Twitter</a>
              <a href="#" className="hover:text-accent">GitHub</a>
              <a href="#" className="hover:text-accent">RSS</a>
            </div>
          </footer>

        </div>
      </body>
    </html>
  );
}

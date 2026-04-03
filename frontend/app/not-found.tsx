import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <h2 className="text-4xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50 sm:text-5xl mb-4">
        404
      </h2>
      <h3 className="text-xl font-medium text-zinc-700 dark:text-zinc-300 mb-8">
        Página no encontrada
      </h3>
      <p className="text-base text-zinc-500 dark:text-zinc-400 mb-10 max-w-md">
        El contenido generado por IA que buscas no existe o ha sido eliminado.
      </p>
      <Link
        href="/"
        className="inline-flex items-center justify-center rounded-md bg-zinc-900 px-6 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-950 focus:ring-offset-2 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
      >
        Volver a la portada
      </Link>
    </div>
  );
}

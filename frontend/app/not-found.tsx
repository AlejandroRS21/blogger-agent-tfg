import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4">
      <span className="text-8xl font-extrabold text-gray-200">404</span>
      <h1 className="-mt-4 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
        Página no encontrada
      </h1>
      <p className="mt-3 max-w-md text-center text-base leading-relaxed text-gray-600">
        Esta página no existe o fue movida. Puede que el post que buscás haya
        sido eliminado o la URL sea incorrecta.
      </p>
      <div className="mt-8 flex items-center gap-4">
        <Link
          href="/"
          className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
        >
          Volver al inicio
        </Link>
        <Link
          href="/archive"
          className="rounded-lg border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
        >
          Ver archivo
        </Link>
      </div>
    </div>
  );
}

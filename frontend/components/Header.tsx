import Link from "next/link";

const navLinks = [
  { href: "/", label: "Blog" },
  { href: "/project", label: "Proyecto" },
  { href: "/generate", label: "Generar" },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200/80 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link href="/" className="group flex items-center gap-2">
          <span className="text-2xl font-extrabold tracking-tight text-gray-900 transition-colors group-hover:text-blue-600">
            BLOGGER<span className="text-blue-600">IA</span>
          </span>
        </Link>

        <nav className="flex items-center gap-6">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
            >
              {link.label}
            </Link>
          ))}
          <a
            href="https://github.com/AlejandroRS21/blogger-agent-tfg"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium text-gray-500 transition-colors hover:text-blue-600"
          >
            GitHub
          </a>
          <a
            href="https://huggingface.co/spaces"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-sm font-medium text-gray-500 transition-colors hover:text-blue-600"
          >
            <span>🤗</span>
            <span className="hidden sm:inline">HF Spaces</span>
          </a>
        </nav>
      </div>
    </header>
  );
}

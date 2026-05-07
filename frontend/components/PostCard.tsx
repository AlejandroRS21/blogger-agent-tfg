import Link from "next/link";
import type { BlogPost } from "@/types/post";

interface PostCardProps {
  post: BlogPost;
}

export default function PostCard({ post }: PostCardProps) {
  const tagColors: Record<string, string> = {
    Tecnologia: "bg-blue-100 text-blue-700",
    Innovacion: "bg-green-100 text-green-700",
    Analisis: "bg-purple-100 text-purple-700",
    Ciencia: "bg-cyan-100 text-cyan-700",
  };

  return (
    <article className="group rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md">
      <Link href={`/posts/${post.slug}`} className="block">
        <h3 className="text-xl font-bold text-gray-900 transition-colors group-hover:text-blue-600">
          {post.title}
        </h3>

        <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-gray-600">
          {post.description}
        </p>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          {post.tags.map((tag) => (
            <span
              key={tag}
              className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
                tagColors[tag] || "bg-gray-100 text-gray-600"
              }`}
            >
              {tag}
            </span>
          ))}
        </div>

        <div className="mt-4 flex items-center gap-4 text-xs text-gray-500">
          <span>{post.date}</span>
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            {post.reading_time} min
          </span>
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {post.word_count} palabras
          </span>
        </div>
      </Link>
    </article>
  );
}

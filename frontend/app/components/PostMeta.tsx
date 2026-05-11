import { PostMetadata } from '../types/post';

interface Props {
  metadata?: PostMetadata;
}

export default function PostMeta({ metadata }: Props) {
  if (!metadata) return null;

  const entries = Object.entries(metadata).filter(([_key, value]) => value !== undefined && value !== null);
  if (entries.length === 0) return null;

  return (
    <section className="my-12 overflow-hidden border border-zinc-100 dark:border-zinc-800 rounded-xl bg-zinc-50/50 dark:bg-zinc-900/30">
      <div className="px-5 py-3 border-b border-zinc-100 dark:border-zinc-800 bg-zinc-100/50 dark:bg-zinc-800/50">
        <h4 className="text-[11px] font-semibold uppercase tracking-[0.2em] text-secondary">
          Métricas de Generación IA
        </h4>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-zinc-100 dark:bg-zinc-800">
        {entries.map(([key, value]) => (
          <div key={key} className="bg-white dark:bg-zinc-900 p-4 flex flex-col gap-1">
            <span className="text-[10px] font-bold uppercase tracking-wider text-secondary opacity-70">
              {key.replace(/_/g, ' ')}
            </span>
            <span className="font-mono text-sm font-semibold text-primary truncate">
              {typeof value === 'number' ? value.toFixed(2) : String(value)}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

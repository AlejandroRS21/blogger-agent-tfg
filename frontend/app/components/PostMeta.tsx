import { PostMetadata } from '../types/post';

interface Props {
  metadata?: PostMetadata;
}

export default function PostMeta({ metadata }: Props) {
  if (!metadata) return null;

  return (
    <div className="my-8 p-4 bg-zinc-50 dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-md text-sm text-zinc-600 dark:text-zinc-400">
      <h4 className="font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Métricas de Generación IA</h4>
      <div className="grid grid-cols-2 gap-2">
        {Object.entries(metadata).map(([key, value]) => (
          <div key={key} className="flex justify-between">
            <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
            <span className="font-mono">{typeof value === 'number' ? value.toFixed(2) : String(value)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

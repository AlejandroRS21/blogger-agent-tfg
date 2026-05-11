import { getAllPosts } from './lib/api';
import PostCard from './components/PostCard';

export const dynamic = 'force-static';

export default async function Home() {
  const posts = await getAllPosts();

  return (
    <div className="space-y-16">
      <section className="text-center py-12 px-4 bg-linear-to-b from-primary/10 via-transparent to-transparent rounded-3xl mb-12 border border-border/20 backdrop-blur-sm">
        <h1 className="text-4xl md:text-6xl font-black text-foreground mb-6 tracking-tight">
          JaviPas <span className="text-primary decoration-primary/30 underline underline-offset-8">AI Clone</span>
        </h1>
        <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Explorando la frontera de la tecnología, IA y gadgets con el estilo inconfundible de Javier Pastor.
        </p>
      </section>

      <div className="flex flex-col max-w-3xl mx-auto">
        {posts.length > 0 ? (
          posts.map((post) => (
            <PostCard key={post.slug} post={post} />
          ))
        ) : (
          <div className="col-span-full py-20 text-center border-2 border-dashed border-border rounded-3xl bg-card/10">
            <p className="text-xl text-muted-foreground italic">
              Todavía no se ha generado ningún post. ¡Ejecuta el agente de IA para empezar!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

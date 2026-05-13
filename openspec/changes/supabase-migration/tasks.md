# Tasks: Supabase Migration

## Phase 1: Infrastructure — Supabase Setup

- [ ] 1.1 Crear proyecto Supabase en https://supabase.com (free tier, región EU)
- [ ] 1.2 Ejecutar SQL de schema en Supabase SQL Editor:
  ```sql
  CREATE TABLE posts (
    id text PRIMARY KEY,
    slug text UNIQUE NOT NULL,
    title text NOT NULL,
    description text,
    content text NOT NULL,
    author text NOT NULL DEFAULT 'Blogger Agent',
    date date NOT NULL,
    word_count integer,
    reading_time integer,
    keywords text[],
    tags text[],
    cover_image_url text,
    created_at timestamptz DEFAULT now()
  );
  ```
- [ ] 1.3 Crear bucket `post-images` en Supabase Storage → configurar como público
- [ ] 1.4 Copiar `SUPABASE_URL` y `SUPABASE_ANON_KEY` del dashboard (Settings → API)

## Phase 2: Backend — Modal webhook INSERT

- [x] 2.1 Añadir `supabase>=2.0.0` a `backend/requirements.txt`
- [x] 2.2 Añadir `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` a `backend/.env.example`
- [x] 2.3 Crear secret `supabase-secret` en Modal dashboard con ambas variables
- [x] 2.4 Añadir `modal.Secret.from_name("supabase-secret")` al `@app.function` del webhook en `modal_app.py`
- [x] 2.5 Implementar `map_to_supabase(result: dict) -> dict` en `modal_app.py` (mapea result dict al schema de posts)
- [x] 2.6 Añadir bloque INSERT en `webhook()` tras `generate_blog_post.remote()`:
  ```python
  from supabase import create_client
  sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
  sb.table("posts").upsert(map_to_supabase(result)).execute()
  ```
- [x] 2.7 Resolver `hf-secret` faltante: crear en Modal o quitar del `@app.function` de `generate_blog_post`

## Phase 3: Frontend — Supabase client + api.ts

- [x] 3.1 Instalar `@supabase/supabase-js`: `cd frontend && npm install @supabase/supabase-js`
- [x] 3.2 Crear `frontend/lib/supabase.ts` con singleton `createClient(URL, ANON_KEY)`
- [x] 3.3 Reescribir `getAllPosts()` en `frontend/lib/api.ts` usando Supabase client (`.from("posts").select("*").order("date", { ascending: false })`)
- [x] 3.4 Reescribir `fetchPost(slug)` en `frontend/lib/api.ts` usando `.from("posts").select("*").eq("slug", slug).single()`
- [x] 3.5 Añadir a `frontend/.env.local`: `NEXT_PUBLIC_SUPABASE_URL=` y `NEXT_PUBLIC_SUPABASE_ANON_KEY=`
- [ ] 3.6 Añadir las mismas env vars a Vercel (Settings → Environment Variables)

## Phase 4: Verification

- [x] 4.1 `modal deploy modal_app.py` — verificar sin errores de secrets
- [x] 4.2 Generar post via `/posts/new` → confirmar row en Supabase table `posts`
- [x] 4.3 Verificar que `/` lista el post generado (lee de Supabase)
- [x] 4.4 Verificar que `/posts/[slug]` renderiza el post individual
- [x] 4.5 Confirmar que error de INSERT retorna `{ success: false }` en el frontend

## Phase 5: Cleanup

- [x] 5.1 Eliminar fetch de GitHub raw de `lib/api.ts` (reemplazado por Supabase)
- [x] 5.2 Commit: `feat(backend): persist posts to Supabase after generation`
- [x] 5.3 Commit: `feat(frontend): read posts from Supabase instead of GitHub raw`

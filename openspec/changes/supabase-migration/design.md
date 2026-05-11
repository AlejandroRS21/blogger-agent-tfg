# Design: Supabase Migration

## Technical Approach

Supabase como única fuente de verdad para posts. Modal webhook hace INSERT tras generar. Frontend usa `@supabase/supabase-js` client-side para reads. Elimina dependencia de GitHub raw y filesystem local (que no persiste en serverless).

## Architecture Decisions

| Decision | Chosen | Rejected | Rationale |
|----------|--------|----------|-----------|
| SDK en backend | `supabase-py` (REST client) | `psycopg2` directo | Menos config, credentials simples (URL+key), igual al SDK de frontend |
| SDK en frontend | `@supabase/supabase-js` | `fetch` manual | Client singleton, realtime ready, tipo-safe |
| Auth en DB | Anon key + RLS disable (TFG) | Service role key expuesto | TFG demo: sin auth de usuario. RLS se añade en producción |
| Upsert strategy | `ON CONFLICT(slug) DO UPDATE` | Error en duplicado | Regenerar mismo tema no rompe el flujo |
| Cover image fase 1 | `cover_image_url` nullable | Bloquear sin imagen | Imágenes son opcionales ahora; columna existe para fase 2 |

## Data Flow

```
Browser ──POST──→ Modal webhook
                      │
                      ├──→ generate_blog_post.remote() ──→ LLM pipeline
                      │                                         │
                      │                                    result dict
                      │                                         │
                      └──→ supabase_client.table("posts")       │
                               .upsert(map_result(result)) ◄────┘
                               │
                          Supabase DB ←── Frontend (getAllPosts / fetchPost)
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/modal_app.py` | Modify | añadir INSERT a Supabase tras `generate_blog_post.remote()` |
| `backend/requirements.txt` | Modify | añadir `supabase>=2.0.0` |
| `frontend/lib/supabase.ts` | Create | singleton client `createClient(URL, ANON_KEY)` |
| `frontend/lib/api.ts` | Modify | `getAllPosts()` y `fetchPost()` usan Supabase client |
| `frontend/.env.local` | Modify | añadir `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` |
| `frontend/package.json` | Modify | añadir `@supabase/supabase-js` |
| `backend/.env.example` | Modify | añadir `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` |

## Interfaces / Contracts

```python
# backend/modal_app.py — helper de mapeo
def map_to_supabase(result: dict) -> dict:
    return {
        "id": result["workflow_id"],
        "slug": result["html_structure"]["metadata"]["slug"],
        "title": result["html_structure"]["metadata"]["title"],
        "description": result["html_structure"]["metadata"]["description"],
        "content": result["html_structure"]["html"],
        "author": "Blogger Agent",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "word_count": result["html_structure"]["metadata"]["word_count"],
        "reading_time": result["html_structure"]["metadata"]["reading_time"],
        "keywords": result.get("keywords", []),
        "tags": result["html_structure"]["metadata"].get("keywords", []),
    }
```

```typescript
// frontend/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `map_to_supabase()` mapeo correcto | pytest con result dict mock |
| Integration | INSERT llega a Supabase | test con Supabase local (`supabase start`) |
| E2E | `getAllPosts()` retorna datos del frontend | verificación manual post-deploy |

## Migration / Rollout

1. Crear proyecto Supabase → ejecutar SQL de schema
2. Configurar `SUPABASE_URL` y `SUPABASE_ANON_KEY` en Modal secrets y Vercel env
3. Deploy backend → deploy frontend
4. Verificar: generar un post → comprobar en Supabase dashboard → comprobar en `/`

No hay migración de datos históricos (docs/ queda como archivo histórico).

## Open Questions

- [ ] ¿Se necesita `SUPABASE_SERVICE_KEY` en Modal o es suficiente con `ANON_KEY` si RLS está desactivado?

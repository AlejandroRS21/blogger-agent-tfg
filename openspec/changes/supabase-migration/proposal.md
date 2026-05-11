# Proposal: Supabase Migration

## Intent

Posts generados vía Modal webhook **no persisten** — `runner.py` escribe a disco local que desaparece al terminar el container serverless. Las imágenes son solo prompts de texto, nunca se generan/almacenan. El frontend lee de GitHub raw (lento, sin queries). Migramos a Supabase: PostgreSQL para posts + Storage para imágenes.

## Scope

### In Scope
- Tabla `posts` en Supabase con todos los campos de `BlogPost`
- Bucket `post-images` en Supabase Storage (CDN público)
- Modal webhook → INSERT en Supabase (reemplaza escritura a disco)
- Frontend `lib/api.ts` → SELECT de Supabase (reemplaza fetch GitHub raw)
- Variables de entorno para Supabase en Modal secrets y Vercel

### Out of Scope
- Generación real de imágenes con IA (solo almacenamos las que existan)
- Auth/RLS por usuario
- Panel de admin para editar posts
- Migración de posts históricos de `docs/`

## Capabilities

### New Capabilities
- `post-persistence`: INSERT/SELECT de posts en Supabase PostgreSQL
- `image-storage`: Upload/retrieve imágenes via Supabase Storage CDN

### Modified Capabilities
- `post-read`: reemplaza fetch de GitHub raw por Supabase client

## Approach

1. Crear proyecto Supabase (free tier) + tabla `posts` + bucket `post-images`
2. Añadir `supabase-py` al backend Modal → `webhook()` hace INSERT tras generar
3. Añadir `@supabase/supabase-js` al frontend → `lib/api.ts` usa Supabase client
4. Secrets: `SUPABASE_URL` + `SUPABASE_ANON_KEY` en Modal y Vercel

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/modal_app.py` | Modified | webhook() → INSERT a Supabase tras generación |
| `backend/requirements.txt` | Modified | añadir `supabase` |
| `frontend/lib/api.ts` | Modified | reemplazar fetch GitHub por Supabase client |
| `frontend/lib/supabase.ts` | New | cliente Supabase singleton |
| `frontend/package.json` | Modified | añadir `@supabase/supabase-js` |
| `frontend/.env.local` | Modified | añadir NEXT_PUBLIC_SUPABASE_URL/ANON_KEY |
| `openspec/config.yaml` | Modified | registrar nuevas capabilities |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Modal timeout antes de INSERT | Med | INSERT al final, tras generación completa |
| Supabase free tier límites (500MB DB, 1GB storage) | Low | suficiente para TFG |
| CORS en Supabase Storage | Low | configurar bucket público con política correcta |
| `hf-secret` faltante bloquea deploy Modal | High | resolver en misma PR: quitar o crear secret |

## Rollback Plan

- `lib/api.ts`: revertir a fetch GitHub raw (1 commit)
- `modal_app.py`: eliminar INSERT block (no rompe generación si falla)
- Supabase: desactivar proyecto (no afecta nada más)

## Dependencies

- Cuenta Supabase (free) con proyecto creado
- `SUPABASE_URL` y `SUPABASE_ANON_KEY` disponibles antes de deploy

## Success Criteria

- [ ] Post generado vía webhook aparece en Supabase tabla `posts`
- [ ] Frontend lista posts desde Supabase (no GitHub raw)
- [ ] `modal deploy` sin errores de secrets
- [ ] Post individual accesible en `/posts/[slug]`

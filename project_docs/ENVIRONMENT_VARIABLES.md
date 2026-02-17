# Configuración de Variables de Entorno

## Frontend (Vercel)

Crea un archivo `.env.local` en el directorio `frontend/` para desarrollo local:

```bash
# Backend API URL (Modal endpoint)
NEXT_PUBLIC_API_URL=https://your-modal-app.modal.run

# Modal Webhook URL (usado en API routes server-side)
MODAL_WEBHOOK_URL=https://your-modal-app.modal.run/webhook

# Opcional: Analytics
NEXT_PUBLIC_ANALYTICS_ID=

# Opcional: Configuración de desarrollo
NODE_ENV=development
```

### Producción (Vercel Dashboard)

Configura estas variables en Vercel Dashboard → Settings → Environment Variables:

| Variable | Entorno | Valor |
|----------|---------|-------|
| `NEXT_PUBLIC_API_URL` | Production, Preview | URL del backend Modal |
| `MODAL_WEBHOOK_URL` | Production, Preview | Webhook del backend Modal |
| `NEXT_PUBLIC_ANALYTICS_ID` | Production | ID de analytics (opcional) |

## Backend (Modal)

Las variables de entorno para Modal se configuran con `modal secret create`:

```bash
# OpenAI API Key
modal secret create openai-secret OPENAI_API_KEY=sk-...

# Anthropic API Key (opcional)
modal secret create anthropic-secret ANTHROPIC_API_KEY=sk-ant-...

# Otras configuraciones
modal secret create app-config \
  VERBOSE=true \
  MAX_RETRIES=3
```

## Notas

- **Variables públicas:** Prefijo `NEXT_PUBLIC_*` se exponen al navegador
- **Variables privadas:** Sin prefijo, solo disponibles en server-side
- **Nunca commitear:** Los archivos `.env*.local` están en `.gitignore`
- **Ejemplo:** Usa `.env.example` como template

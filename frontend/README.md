# Frontend - Blogger Agent TFG

:warning: **IMPORTANTE: Este directorio contiene un frontend Next.js que YA NO SE UTILIZA**

## :information_source: Estado Actual

El proyecto ahora utiliza **GitHub Pages con HTML estático** en lugar de Next.js.

- **Frontend activo**: `/docs` (HTML, CSS, JavaScript vanilla)
- **URL de producción**: [https://alejandroors21.github.io/blogger-agent-tfg/](https://alejandroors21.github.io/blogger-agent-tfg/)
- **Deployment**: Automático vía GitHub Pages

## :question: ¿Por qué se cambió?

1. **Simplicidad**: No requiere Node.js, npm, ni proceso de build
2. **Rendimiento**: Carga instantánea sin bundling
3. **Costos**: GitHub Pages es completamente gratuito
4. **Mantenimiento**: Menos dependencias y actualizaciones

## :recycle: Este directorio Next.js

Este directorio se mantiene como **referencia histórica** y podría reutilizarse en el futuro si se necesitan funcionalidades más avanzadas como:

- Generación dinámica de contenido desde el frontend
- API routes para integración con backend
- Sistema de autenticación
- Panel de administración

## :rocket: Ver el Frontend Actual

Para ver el frontend en producción:
- **URL**: [https://alejandroors21.github.io/blogger-agent-tfg/](https://alejandroors21.github.io/blogger-agent-tfg/)
- **Código fuente**: Directorio `/docs` en la raíz del proyecto

Para desarrollo local del frontend actual:
```bash
cd docs
python -m http.server 8000
# → http://localhost:8000
```

---

## :page_facing_up: Documentación Original (Next.js - No Usado)

<details>
<summary>Expandir para ver la documentación del frontend Next.js (archivado)</summary>

## 🚀 Quick Start

```bash
cd frontend
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## 📁 Estructura del Proyecto

```
frontend/
├── app/
│   ├── api/
│   │   └── generate-post/
│   │       └── route.ts          # API endpoint para generar posts
│   ├── components/
│   │   ├── BlogLayout.tsx        # Layout principal (header/footer)
│   │   ├── PostHeader.tsx        # Encabezado de posts con metadata
│   │   ├── PostBody.tsx          # Renderizado de contenido HTML
│   │   └── GenerateForm.tsx      # Formulario de generación
│   ├── generate/
│   │   └── page.tsx              # Página del formulario
│   ├── posts/
│   │   └── [slug]/
│   │       └── page.tsx          # Página dinámica de posts
│   ├── types/
│   │   └── post.ts               # TypeScript types
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Homepage
│   └── globals.css               # Estilos globales
├── public/                       # Assets estáticos
├── .env.local                    # Variables de entorno
├── package.json
└── tailwind.config.ts
```

## 🎨 Componentes

### `BlogLayout`
Layout principal con navegación y footer.

**Props:** `children: React.ReactNode`

### `PostHeader`
Muestra título, descripción y metadata del post.

**Props:**
- `title: string`
- `description: string`
- `date: string`
- `readingTime: number`
- `wordCount: number`
- `author?: string`
- `tags?: string[]`

### `PostBody`
Renderiza el contenido HTML del post con estilos prose de Tailwind.

**Props:** `htmlContent: string`

### `GenerateForm`
Formulario para generar posts. Envía datos al endpoint `/api/generate-post`.

**Campos:**
- Nombre del blogger
- Biografía
- Posts de ejemplo (URLs)
- Tema del post
- Palabras clave (opcional)

## 🔌 API Routes

### `POST /api/generate-post`

Genera un post usando el backend Python.

**Request Body:**
```typescript
{
  blogger_name: string;
  blogger_bio: string;
  blogger_sample_posts: string[];
  topic: string;
  keywords?: string[];
}
```

**Response:**
```typescript
{
  success: boolean;
  post?: BlogPost;
  error?: string;
  execution_time?: number;
}
```

## 🌐 Páginas

### `/` - Homepage
Página principal con hero, features y tech stack.

### `/generate` - Generación
Formulario para crear nuevos posts.

### `/posts/[slug]` - Post dinámico
Muestra un post generado.

## ⚙️ Configuración

### Variables de Entorno (`.env.local`)

```bash
# Backend URL (local o Modal webhook)
BACKEND_URL=http://localhost:8000

# Modo mock (true para desarrollo sin backend)
USE_MOCK=true

# App metadata
NEXT_PUBLIC_APP_NAME=Blogger Agent TFG
NEXT_PUBLIC_APP_DESCRIPTION=Sistema multi-agente para generar contenido
```

## 🔧 Scripts

- `npm run dev` - Servidor de desarrollo (port 3000)
- `npm run build` - Build de producción
- `npm run start` - Servidor de producción
- `npm run lint` - ESLint

## 🎯 Modo Mock vs Modo Real

### Modo Mock (desarrollo)
```bash
USE_MOCK=true
```
- No requiere backend corriendo
- Genera posts de ejemplo
- Delay simulado de 2 segundos

### Modo Real (producción)
```bash
USE_MOCK=false
BACKEND_URL=http://localhost:8000  # o Modal webhook
```
- Conecta con el backend Python
- Usa agentes de IA reales
- Tiempo de ejecución variable

## 🧪 Testing

Para probar el flujo completo:

1. **Iniciar frontend:**
   ```bash
   npm run dev
   ```

2. **Modo Mock (sin backend):**
   - Abre http://localhost:3000
   - Navega a "Generar Post"
   - Llena el formulario
   - Observa el post generado

3. **Modo Real (con backend):**
   ```bash
   # Terminal 1: Backend
   cd ../backend
   uv run uvicorn aphra_blogger.api:app --reload

   # Terminal 2: Frontend
   npm run dev
   ```

## 📦 Dependencias Principales

- **Next.js 16.1.6** - React framework
- **React 19.2.3** - UI library
- **TypeScript 5** - Type safety
- **Tailwind CSS 4** - Styling

## 🚢 Deploy

### Vercel (recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Variables de entorno en Vercel:
- `BACKEND_URL`: URL del backend en Modal
- `USE_MOCK`: `false` para producción

## 📚 Recursos

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript](https://www.typescriptlang.org)

</details>

---

**Última actualización**: 17 de febrero de 2026  
**Estado**: :no_entry: Archivado (se usa GitHub Pages en su lugar)

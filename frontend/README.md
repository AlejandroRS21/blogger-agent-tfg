# Frontend - Blogger Agent TFG

Frontend estático de Next.js 16 para el sistema multi-agente de generación de contenido de blog.

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
│   ├── components/
│   │   ├── HTMLRenderer.tsx       # Renderizado de contenido HTML con sanitización
│   │   ├── PostCard.tsx           # Tarjeta de post para listados (homepage)
│   │   └── PostMeta.tsx           # Metadata de posts (fecha, etiquetas, autor)
│   ├── posts/
│   │   └── [slug]/
│   │       └── page.tsx           # Página dinámica de post individual
│   ├── lib/
│   │   ├── api.ts                 # Data fetching layer
│   │   └── postAudit.ts           # Post integrity checks
│   ├── types/
│   │   └── post.ts                # Zod schemas + TypeScript types
│   ├── layout.tsx                 # Root layout con nav y footer
│   ├── page.tsx                   # Homepage (grid de PostCards)
│   ├── not-found.tsx              # 404 page
│   └── globals.css                # Estilos globales Tailwind v4
├── __tests__/                     # Tests con Jest + Testing Library
│   ├── api.test.ts
│   ├── HTMLRenderer.test.tsx
│   ├── PostCard.test.tsx
│   ├── integrity.test.ts
│   └── seo.test.ts
├── public/                        # Assets estáticos
├── package.json
├── next.config.ts                 # Static export + React Compiler
├── jest.config.ts
├── jest.setup.ts
└── tsconfig.json
```

## 🎨 Componentes

### `HTMLRenderer`
Renderiza contenido HTML sanitizado con estilos prose de Tailwind.

**Props:** `htmlContent: string`

### `PostCard`
Tarjeta de presentación para listados de posts en la homepage.

**Props:** `post: PostListItem`

### `PostMeta`
Muestra título, descripción y metadata del post.

**Props:**
- `title: string`
- `description?: string`
- `date: string`
- `tags?: string[]`

## 🌐 Páginas

### `/` - Homepage
Página principal con hero section y grid de posts usando `PostCard`.

### `/posts/[slug]` - Post dinámico
Muestra un post individual con su contenido HTML renderizado.

## ⚙️ Configuración

### Variables de Entorno (`.env.local`)

Crea este archivo si no existe:

```bash
# Backend URL (Modal webhook)
BACKEND_URL=http://localhost:8000

# Modo mock (true para desarrollo sin backend)
USE_MOCK=true

# App metadata
NEXT_PUBLIC_APP_NAME=Blogger Agent TFG
NEXT_PUBLIC_APP_DESCRIPTION=Sistema multi-agente para generar contenido
```

## 🔧 Scripts

- `npm run dev` - Servidor de desarrollo (port 3000)
- `npm run build` - Build de producción (static export a `out/`)
- `npm run start` - Servidor de producción
- `npm run lint` - ESLint
- `npm test` - Jest + Testing Library

## 🧪 Testing

Tests implementados con Jest + Testing Library:

```bash
# Ejecutar todos los tests
npm test

# Con coverage
npm test -- --coverage
```

Archivos de test:
- `api.test.ts` — Tests de la capa de datos
- `HTMLRenderer.test.tsx` — Tests del renderizador HTML
- `PostCard.test.tsx` — Tests de la tarjeta de posts
- `integrity.test.ts` — Tests de integridad de datos
- `seo.test.ts` — Tests de SEO y metadata

## 📦 Dependencias Principales

- **Next.js 16.1.6** — React framework con App Router
- **React 19.2.3** — UI library
- **TypeScript 5** — Type safety
- **Tailwind CSS 4** — Utility-first styling
- **isomorphic-dompurify** — Sanitización HTML
- **Zod 4** — Validación de schemas

## 🚢 Deploy

### Static Export

El proyecto usa `output: 'export'` para generar un sitio completamente estático en `out/`.

```bash
npm run build
# La salida está en out/
```

### Vercel

```bash
npm i -g vercel
vercel
```

Configuración en `vercel.json` (raíz del proyecto).

## 📚 Recursos

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS v4](https://tailwindcss.com)
- [TypeScript](https://www.typescriptlang.org)

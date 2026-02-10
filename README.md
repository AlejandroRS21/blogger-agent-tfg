# Blogger Agent TFG

> Multi-agent AI system for mimicking blogger writing style using Aphra workflows, Next.js, and Modal deployment

## 📋 Descripción del Proyecto

Sistema multi-agente de IA que analiza el estilo de escritura de un blogger y genera artículos nuevos que mimetizan su tono, estructura, y forma de escribir. El proyecto utiliza múltiples agentes especializados que colaboran para:

- Analizar el estilo narrativo del blogger
- Extraer palabras clave y patrones lingüísticos
- Generar contenido base
- Criticar y refinar el texto
- Construir HTML/JSX optimizado para Next.js
- Seleccionar y ubicar imágenes apropiadas

## 🏗️ Arquitectura

```
blogger-agent-tfg/
├── backend/                    # Python + Aphra Workflows
│   ├── aphra_blogger/
│   │   ├── workflows/
│   │   │   ├── blogger_style.py
│   │   │   ├── agents/
│   │   │   │   ├── style_analyzer.py
│   │   │   │   ├── keyword_extractor.py
│   │   │   │   ├── content_generator.py
│   │   │   │   ├── critic.py
│   │   │   │   ├── html_builder.py
│   │   │   │   └── image_selector.py
│   │   │   └── prompts/
│   │   ├── config/
│   │   └── context.py
│   ├── runner.py
│   ├── requirements.txt
│   └── tests/
├── frontend/                   # Next.js
│   ├── app/
│   │   ├── api/
│   │   │   └── generate-post/
│   │   ├── posts/[slug]/
│   │   └── components/
│   ├── package.json
│   └── next.config.js
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── SETUP.md
│   └── _DEPLOYMENT.md
├── docker-compose.yml
└── CONTRIBUTING.md
```

## 👥 División de Tareas (3 Personas)

### 👤 Persona 1: Backend Lead + Workflows Core
**Responsabilidades:**
- Estructura base del `BloggerStyleWorkflow`
- Agentes principales:
  - `style_analyzer.py` - Análisis del estilo del blogger
  - `content_generator.py` - Redacción base + refinada  
  - `critic.py` - Crítica y feedback
- Configuración de `config/default.toml`
- Tests unitarios backend
- Docker setup para backend

**Branches:**
- `feature/workflow-base`
- `feature/style-analyzer`
- `feature/content-generator`
- `feature/critic-agent`

### 👤 Persona 2: Backend Specialization + Integration  
**Responsabilidades:**
- Agentes especializados:
  - `keyword_extractor.py` - Palabras clave y términos
  - `html_builder.py` - Construcción JSON/HTML
  - `image_selector.py` - Descripciones de imágenes
- Prompts tuneados en `prompts/`
- `runner.py` - CLI para ejecutar workflows
- Tests de integración
- Documentación técnica (`ARCHITECTURE.md`, `API.md`)
## 🏛️ Next.js como Motor del Blog

**IMPORTANTE**: Este proyecto **NO usa WordPress**. El blog completo está construido con **Next.js 14** usando App Router.

### Arquitectura del Blog

```
Backend (Modal)          Frontend (Next.js Blog)
┌──────────────────┐       ┌────────────────────────┐
│ Workflow Agentes │       │ Next.js App           │
│ + Modal Deploy   │  -->  │ + Markdown Rendering  │
│                  │       │ + SEO Optimizado      │
│ Genera JSON      │       │ + Componentes React   │
└──────────────────┘       └────────────────────────┘
```

### Flujo de Generación y Publicación

1. **Usuario solicita generar post** (UI de Next.js)
2. **API Route** (`/api/generate-post`) llama al webhook de Modal
3. **Modal ejecuta workflow** con agentes (style_analyzer, content_generator, etc.)
4. **Modal devuelve JSON** estructurado:
   ```json
   {
     "slug": "mi-experiencia-con-claude-opus",
     "title": "Claude Opus me tiene un poco alucinado",
     "description": "Mis primeras impresiones tras...",
     "content_markdown": "## Intro\n\nTotal, que...",
     "meta": {
       "author": "Sistema Blogger Agent",
       "date": "2026-02-10",
       "tags": ["ia", "claude", "anthropic"],
       "read_time": "8 min"
     },
     "images": [
       {
         "id": "hero",
         "alt": "Claude Opus interface",
         "position": "hero"
       }
     ]
   }
   ```
5. **Next.js guarda el post** en el filesystem o base de datos
6. **Next.js renderiza el post** en `/posts/[slug]` usando:
   - Server Components para SEO
   - Markdown → HTML con `remark`/`rehype`
   - Metadata dinámica para `<head>`

### Estructura Frontend Next.js

```typescript
// app/posts/[slug]/page.tsx
import { getPost } from '@/lib/posts';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { BlogLayout } from '@/components/BlogLayout';

export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.description,
    openGraph: {
      title: post.title,
      description: post.description,
      type: 'article'
    }
  };
}

export default async function PostPage({ params }) {
  const post = await getPost(params.slug);
  
  return (
    <BlogLayout>
      <article>
        <h1>{post.title}</h1>
        <div className="meta">
          <time>{post.meta.date}</time>
          <span>{post.meta.read_time}</span>
        </div>
        <MarkdownRenderer content={post.content_markdown} />
      </article>
    </BlogLayout>
  );
}
```

### Almacenamiento de Posts

**Opción 1: Filesystem (más simple para el TFG)**
```
frontend/
└── content/
    └── posts/
        ├── mi-experiencia-con-claude.json
        ├── anthropic-es-la-nueva-apple.json
        └── ...
```

**Opción 2: Base de datos (más escalable)**
- Vercel Postgres / Supabase
- Tabla `posts` con columnas: `slug`, `title`, `content`, `meta`, etc.

### Ventajas de Next.js vs WordPress

✅ **Performance**: Server Components, Static Generation  
✅ **TypeScript**: Type-safe en todo el stack  
✅ **Control total**: Sin limitaciones de plugins  
✅ **SEO moderno**: Metadata API, sitemap automático  
✅ **Deploy fácil**: Vercel, Netlify, Railway  
✅ **Sin base de datos MySQL**: Opcional, no obligatorio  
✅ **Markdown nativo**: Renderizado con remark/rehype  
✅ **Componentes reutilizables**: React ecosystem

### Componentes Principales

- **`<BlogLayout>`**: Layout general con header, footer, sidebar
- **`<PostHeader>`**: Hero image, título, meta (autor, fecha, lectura)
- **`<PostBody>`**: Renderizado de markdown con estilos
- **`<RelatedPosts>`**: Algoritmo simple de posts relacionados
- **`<ImageCarousel>`**: Galería de imágenes del post
- **`<CommentSection>`**: Sistema de comentarios (Giscus/Disqus/custom)


- **Integración con Modal** para deployment
- **Integración con Vercel** para deployment del frontend Next.js

**Branches:**
- `feature/keyword-extractor`
- `feature/html-builder`  
- `feature/image-selector`
- `feature/runner-cli`
- `feature/modal-deployment`
- `docs/architecture`

### 👤 Persona 3: Frontend Full Stack + DevOps
**Responsabilidades:**
- Frontend completo Next.js:
  - Componentes React (`<BlogLayout>`, `<PostHeader>`, `<PostBody>`, etc.)
  - Página dinámica `app/posts/[slug]/page.tsx`
  - API route `app/api/generate-post/route.ts`
  - Estilos y UX (Tailwind CSS)
- DevOps:
  - `docker-compose.yml` completo
  - GitHub Actions CI/CD
  - `SETUP.md` y `DEPLOYMENT.md`
- Testing frontend

**Branches:**
- `feature/blog-components`
- `feature/post-page`
- `feature/api-endpoint`
- `feature/docker-setup`
- `feature/ci-cd`
- `docs/setup`

## 🚀 Integración con Modal

**Modal** se usará para deployment serverless del backend Python:

### ¿Por qué Modal?
- Ejecución serverless de código Python
- Escalado automático según demanda
- Gestión de dependencias integrada
- GPU/CPU bajo demanda para LLMs
- Costos eficientes (pay-per-use)

### Implementación

```python
# backend/modal_app.py
import modal

stub = modal.Stub("blogger-agent")

image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt")

@stub.function(image=image, secrets=[modal.Secret.from_name("openai-secret")])
def generate_blog_post(blogger_urls: list[str], topic: str) -> dict:
    from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow
    
    workflow = BloggerStyleWorkflow()
    result = workflow.run(blogger_urls=blogger_urls, topic=topic)
    
    return result

@stub.webhook(method="POST")
def webhook(data: dict):
    result = generate_blog_post.call(
        blogger_urls=data["blogger_urls"],
        topic=data["topic"]
    )
    return result
```

### Conexión Next.js → Modal

```typescript
// frontend/app/api/generate-post/route.ts
export async function POST(request: Request) {
  const { bloggerUrls, topic } = await request.json();
  
  const response = await fetch(process.env.MODAL_WEBHOOK_URL!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ blogger_urls: bloggerUrls, topic })
  });
  
  const post = await response.json();
  return Response.json(post);
}
```

## 🔧 Setup Rápido

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python runner.py --blogger-urls https://example.com/blog --topic "AI en educación"
```

### Frontend  
```bash
cd frontend
npm install
npm run dev
```

### Docker (Todo junto)
```bash
docker-compose up
```

### Modal Deployment
```bash
modal deploy backend/modal_app.py
```

## 📊 Flujo de Trabajo (Workflow)

1. **Análisis de Estilo** (`style_analyzer`) → Analiza posts del blogger
2. **Extracción de Keywords** (`keyword_extractor`) → Palabras clave recurrentes
3. **Generación Base** (`content_generator`) → Primer borrador
4. **Aplicación de Estilo** (`content_generator`) → Reescribe con estilo del blogger
5. **Crítica** (`critic`) → Feedback sobre coherencia y estilo  
6. **Refinamiento** (`content_generator`) → Versión final
7. **HTML Builder** (`html_builder`) → Estructura JSON/HTML
8. **Selección de Imágenes** (`image_selector`) → Prompts y ubicaciones

## 🤝 Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para entender el flujo de trabajo con Git y GitHub.

### Flujo Git
1. Crear issue desde GitHub Projects
2. Asignarte la issue
3. Crear rama: `git checkout -b feature/nombre`
4. Commits: `git commit -m "feat(scope): description"`
5. Push y PR contra `develop`
6. Esperar 1 approval
7. Merge

## 📚 Documentación

- [Arquitectura](docs/ARCHITECTURE.md) - Diseño del sistema
- [API](docs/API.md) - Especificación de agentes y workflows
- [Setup](docs/SETUP.md) - Configuración detallada
- [Modal Deployment](docs/MODAL_DEPLOYMENT.md) - Guía de deployment

## 🧪 Testing

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend  
npm test
```

## 📦 Tech Stack

### Backend
- Python 3.11+
- Aphra (workflow framework)
- OpenAI API / OpenRouter
- Modal (serverless deployment)
- pytest

### Frontend
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Jest + Testing Library

### DevOps
- Docker + Docker Compose
- GitHub Actions
- Modal

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 👨‍🎓 Proyecto Académico

Trabajo Final de Grado (TFG) - Especialización en IA y Big Data  
IES Rafael Alberti - 2026

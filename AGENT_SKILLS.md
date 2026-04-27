# Agent Skills - Blogger Agent TFG

Este documento define las **skills (habilidades/capacidades)** necesarias para cada tipo de agente en el flujo de trabajo del proyecto. Estas skills ayudan a GitHub Copilot y otros agentes de IA a entender mejor el contexto y las tareas de cada rol.

## 👥 Estructura de Equipos y Skills

### **Persona 1: Backend & Infrastructure Lead (P1)**

#### Skills Principales:
- **aphra-workflows**: Diseño y desarrollo de workflows con Aphra para orquestación de agentes
- **modal-deployment**: Configuración y despliegue de aplicaciones en Modal.com
- **python-backend**: Desarrollo de backend en Python con FastAPI
- **docker-containerization**: Containerización de aplicaciones con Docker
- **api-design**: Diseño de APIs RESTful para comunicación entre servicios
- **database-management**: Gestión de bases de datos (PostgreSQL, MongoDB)
- **environment-config**: Configuración de variables de entorno y secrets
- **ci-cd-setup**: Configuración de pipelines de CI/CD

#### Tareas Asignadas:
- ✅ Issue #1: Setup proyecto base y estructura de workflows
- 📄 Issue #5: Configurar Modal para deployment del backend

#### Comandos y Herramientas:
```bash
# Aphra CLI
aphra init
aphra workflow create <name>
aphra agent add <agent-name>

# Modal CLI
modal setup
modal deploy
modal run <app>::<function>

# Docker
docker build -t blogger-agent .
docker-compose up -d
```

---

### **Persona 2: Content Analysis & Agents Lead (P2)**

#### Skills Principales:
- **nlp-analysis**: Análisis de lenguaje natural (NLP) con spaCy, NLTK, Transformers
- **web-scraping**: Extracción de contenido web con BeautifulSoup, Scrapy, Playwright
- **content-mimicry**: Técnicas de imitación de estilo de escritura
- **llm-prompting**: Ingeniería de prompts para LLMs (HuggingFace, GPT, Gemini)
- **style-transfer**: Transfer learning para adaptación de estilo
- **sentiment-analysis**: Análisis de sentimiento y tono
- **text-generation**: Generación de texto con modelos de lenguaje
- **data-preprocessing**: Preprocesamiento de texto y limpieza de datos
- **agent-orchestration**: Coordinación de múltiples agentes con Aphra

#### Tareas Asignadas:
- 📄 Issue #2: [Research] Análisis del blog de Javi Pas (javipas.com)
- 📄 Issue #6: Desarrollar agentes de análisis de contenido
- 📄 Issue #7: Implementar agentes de generación de contenido

#### Agentes Implementados:

**1. StyleAnalyzer**
```python
# Fichero: style_analyzer.py
# Skill: tone-style-analysis
# Analiza tono, voz, estructura narrativa y expresiones características
# Tecnologías: spaCy, Transformers, LLM prompts
```

**2. KeywordExtractor**
```python
# Fichero: keyword_extractor.py
# Skill: keyword-extraction
# Extrae palabras clave, expresiones y temáticas del contenido analizado
# Tecnologías: NLTK, TF-IDF, RAKE, LLM
```

**3. ContentGenerator**
```python
# Fichero: content_generator.py
# Skill: content-generation
# Genera borradores, refina contenido y aplica mimicry de estilo
# Soporta modos: REFLECTIVE, TECHNICAL, QUICK_FLASH, CURATED_LINKS, RANT
# Tecnologías: HuggingFace, OpenAI, Gemini, Modal
```

**4. CriticAgent**
```python
# Fichero: critic.py
# Skill: content-critique
# Evalúa coherencia, ajuste de estilo y engagement del texto generado
# Tecnologías: LLM prompts, readability scores, quality metrics
```

**5. ImageSelectorAgent**
```python
# Fichero: image_selector.py
# Skill: image-selection
# Selecciona imágenes relevantes y genera prompts para el artículo
# Tecnologías: Brave Search API, perception model, prompt templates
```

**6. HTMLBuilder**
```python
# Fichero: html_builder.py
# Skill: html-building
# Convierte Markdown → HTML, genera TOC, meta tags y estructura JSX
# Tecnologías: HTML parsing, meta tag generation, JSX conversion
```

**7. ResearchAgent**
```python
# Fichero: research_agent.py
# Skill: research-topic
# Busca información actualizada y contexto para los artículos
# Tecnologías: Brave Search API, web scraping, LLM summarization
```

#### Proveedores LLM:

| Proveedor | Fichero | Prioridad | Modelo por Defecto |
|-----------|---------|-----------|-------------------|
| HuggingFace | `huggingface_provider.py` | Primario (gratuito) | `meta-llama/Meta-Llama-3.1-8B-Instruct` |
| OpenAI | `openai_provider.py` | Fallback | `gpt-4-turbo-preview` |
| Gemini | `gemini_provider.py` | Alternativa | `gemini-2.0-flash` |
| Modal | `modal_provider.py` | Hosting propio | `blogger-agent-models/LlamaModel.generate` |

#### Bibliotecas Python Clave:
```python
import spacy
import nltk
from transformers import pipeline, AutoTokenizer, AutoModel
from bs4 import BeautifulSoup
from huggingface_hub import InferenceClient
from openai import OpenAI
from google import genai
import modal
```

---

### **Persona 3: Frontend & Next.js Lead (P3)**

#### Skills Principales:
- **nextjs-development**: Desarrollo de aplicaciones con Next.js 16+ (App Router)
- **react-components**: Creación de componentes React 19 reutilizables
- **tailwindcss-styling**: Estilizado con Tailwind CSS 4
- **html-css-extraction**: Extracción y adaptación de HTML/CSS de sitios web
- **responsive-design**: Diseño responsive y mobile-first
- **seo-optimization**: Optimización para motores de búsqueda
- **performance-optimization**: Optimización de rendimiento web
- **api-integration**: Integración con APIs backend
- **markdown-rendering**: Renderizado de contenido Markdown
- **static-generation**: Generación estática con Next.js SSG

#### Tareas Asignadas:
- 📄 Issue #4: Implementar blog completo en Next.js (Motor del blog - NO WordPress)
- 📄 Issue #8: Copiar y adaptar HTML/CSS del blog javipas.com

#### Comandos y Herramientas:
```bash
# Next.js
npx create-next-app@latest blogger-agent-frontend
npm run dev
npm run build
npm run start

# Tailwind CSS 4
npx @tailwindcss/cli init

# Testing
npm run test

# Deployment
vercel deploy
```

#### Estructura de Componentes:
```typescript
// Skills: component-architecture, typescript

app/
├── components/
│   ├── HTMLRenderer.tsx      # Renderiza HTML sanitizado con DOMPurify
│   ├── PostCard.tsx           # Tarjetas de post para la lista
│   └── PostMeta.tsx           # Metadatos del post (tags, fechas, etc.)
├── posts/
│   └── [slug]/
│       └── page.tsx           # Página de detalle del post
├── types/
│   └── post.ts                # Tipos PostMetadata, PostListItem
├── layout.tsx                 # Layout raíz con Header/Footer + SEO
├── not-found.tsx              # Página 404 personalizada
└── page.tsx                   # Home con listado de posts
```

#### Bibliotecas y Paquetes:
```json
{
  "dependencies": {
    "next": "16.1.6",
    "react": "19.2.3",
    "react-dom": "19.2.3",
    "zod": "^4.3.6",
    "isomorphic-dompurify": "^3.7.1",
    "@tailwindcss/typography": "^0.5.19"
  },
  "devDependencies": {
    "typescript": "^5",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "jest": "^30.3.0",
    "@testing-library/react": "^16.3.2",
    "eslint": "^9",
    "eslint-config-next": "16.1.6"
  }
}
```

---

## 🤖 Configuración de GitHub Copilot

### Instrucciones Personalizadas por Rol

Para maximizar la efectividad de GitHub Copilot, cada miembro del equipo debe configurar instrucciones personalizadas:

#### Para P1 (Backend Lead):
```
I'm working on a multi-agent AI system backend using Aphra workflows and Modal deployment.
Focus on:
- Python backend code with type hints
- Aphra workflow definitions
- Modal deployment configurations
- Docker containerization
- API endpoint design
```

#### Para P2 (Content Analysis Lead):
```
I'm developing NLP agents for content analysis and text generation using multiple LLM providers.
Focus on:
- NLP tasks with spaCy, NLTK, Transformers
- LLM prompt engineering (HuggingFace, OpenAI, Gemini, Modal)
- Web scraping with BeautifulSoup
- Style mimicry and structured content generation
- Aphra agent definitions
- DO NOT use Anthropic/Claude — we use HuggingFace (primary), OpenAI (fallback), Gemini, or Modal providers
```

#### Para P3 (Frontend Lead):
```
I'm building a Next.js 16 blog with App Router and Tailwind CSS 4.
Focus on:
- Next.js 16 App Router patterns
- React 19 Server Components and Server Actions
- Tailwind CSS 4 styling (no @apply, use CSS variables via @theme)
- TypeScript 5 type safety
- DOMPurify for HTML sanitization
- Responsive design with Geist font
- Jest + React Testing Library for tests
```

---

## 📦 Dependencias del Proyecto

### Backend (P1)
```txt
aphra>=0.1.0
modal>=0.55.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
python-dotenv>=1.0.0
toml>=0.10.0
```

### Agents (P2)
```txt
spacy>=3.7.0
nltk>=3.8.0
transformers>=4.35.0
beautifulsoup4>=4.12.0
huggingface-hub>=0.20.0
openai>=1.3.0
google-genai>=1.0.0
modal>=0.55.0
requests>=2.31.0
```

### Frontend (P3)
```json
{
  "next": "16.1.6",
  "react": "19.2.3",
  "tailwindcss": "^4",
  "typescript": "^5"
}
```

---

## 📝 Workflow de Colaboración

### 1. Sincronización de Trabajo
- **Daily standups**: Revisión de progreso en Issues
- **Pull Requests**: Revisar código entre miembros
- **Kanban Board**: Mover issues entre columnas (Backlog → In Progress → In Review → Done)

### 2. Convenciones de Código
- **Commits**: `[P1/P2/P3] Descripción del cambio`
- **Branches**: `feature/p1-modal-setup`, `feature/p2-nlp-agents`, `feature/p3-nextjs-blog`
- **PRs**: Template con checklist de tareas completadas

### 3. Testing
- **P1**: Pytest para backend y workflows
- **P2**: Unit tests para agentes individuales
- **P3**: Jest + React Testing Library para componentes

---

## 🔗 Enlaces Útiles

- **Aphra Docs**: https://github.com/aphra-ai/aphra
- **Modal Docs**: https://modal.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Blog Objetivo**: https://javipas.com/
- **Geist Font**: https://vercel.com/font

---

## 🎯 Objetivos del Proyecto

1. **Análisis completo** del estilo de escritura de javipas.com
2. **Sistema multi-agente** funcional con Aphra
3. **Generación automática** de artículos que imiten el estilo
4. **Blog Next.js 16** con diseño similar al original
5. **Deployment funcional** en Modal y Vercel
6. **Documentación completa** del TFG

---

**Última actualización**: 27 de abril de 2026

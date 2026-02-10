# Agent Skills - Blogger Agent TFG

Este documento define las **skills (habilidades/capacidades)** necesarias para cada tipo de agente en el flujo de trabajo del proyecto. Estas skills ayudan a GitHub Copilot y otros agentes de IA a entender mejor el contexto y las tareas de cada rol.

## 👥 Estructura de Equipos y Skills

### **Persona 1: Backend & Infrastructure Lead (P1)**

#### Skills Principales:
- **aphra-workflows**: Diseño y desarrollo de workflows con Aphra para orquestación de agentes
- **modal-deployment**: Configuración y despliegue de aplicaciones en Modal.com
- **python-backend**: Desarrollo de backend en Python con FastAPI/Flask
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
- **llm-prompting**: Ingeniería de prompts para LLMs (GPT, Claude, Llama)
- **style-transfer**: Transfer learning para adaptación de estilo
- **sentiment-analysis**: Análisis de sentimiento y tono
- **text-generation**: Generación de texto con modelos de lenguaje
- **data-preprocessing**: Preprocesamiento de texto y limpieza de datos
- **agent-orchestration**: Coordinación de múltiples agentes con Aphra

#### Tareas Asignadas:
- 📄 Issue #2: [Research] Análisis del blog de Javi Pas (javipas.com)
- 📄 Issue #6: Desarrollar agentes de análisis de contenido
- 📄 Issue #7: Implementar agentes de generación de contenido

#### Agentes a Implementar:

**1. Agente de Análisis de Tono y Estilo**
```python
# Skill: tone-style-analysis
# Analiza el tono, formalidad, humor y estilo narrativo
# Tecnologías: spaCy, Transformers, custom classifiers
```

**2. Agente de Análisis de Temáticas**
```python
# Skill: topic-modeling
# Extrae temáticas principales usando LDA, NMF, BERTopic
# Tecnologías: gensim, scikit-learn, BERTopic
```

**3. Agente de Palabras Frecuentes**
```python
# Skill: frequency-analysis
# Identifica palabras, expresiones y muletillas características
# Tecnologías: NLTK, collections.Counter, TF-IDF
```

**4. Agente Generador de Texto Base**
```python
# Skill: base-text-generation
# Genera borrador inicial del artículo
# Tecnologías: GPT-4, Claude, Llama
```

**5. Agente de Mimesis**
```python
# Skill: style-mimicry
# Adapta el texto al estilo del blogger objetivo
# Tecnologías: Fine-tuned LLM, prompt engineering
```

**6. Agente Crítico**
```python
# Skill: content-critique
# Revisa y sugiere mejoras al texto generado
# Tecnologías: GPT-4, quality metrics, readability scores
```

**7. Agente de Selección de Imágenes**
```python
# Skill: image-selection
# Selecciona imágenes relevantes para el artículo
# Tecnologías: CLIP, Unsplash API, stable-diffusion
```

#### Bibliotecas Python Clave:
```python
import spacy
import nltk
from transformers import pipeline, AutoTokenizer, AutoModel
from bs4 import BeautifulSoup
import scrapy
from langchain import LLMChain, PromptTemplate
import openai
import anthropic
```

---

### **Persona 3: Frontend & Next.js Lead (P3)**

#### Skills Principales:
- **nextjs-development**: Desarrollo de aplicaciones con Next.js 14+ (App Router)
- **react-components**: Creación de componentes React reutilizables
- **tailwindcss-styling**: Estilizado con Tailwind CSS
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

# Tailwind CSS
npx tailwindcss init -p

# Deployment
vercel deploy
```

#### Estructura de Componentes:
```typescript
// Skills: component-architecture, typescript

components/
├── layout/
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── Layout.tsx
├── blog/
│   ├── PostCard.tsx
│   ├── PostContent.tsx
│   ├── PostMeta.tsx
│   └── PostList.tsx
└── ui/
    ├── Button.tsx
    ├── Image.tsx
    └── Link.tsx
```

#### Bibliotecas y Paquetes:
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "gray-matter": "^4.0.3",
    "remark": "^15.0.0",
    "remark-html": "^16.0.0",
    "date-fns": "^3.0.0"
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
I'm developing NLP agents for content analysis and text generation.
Focus on:
- NLP tasks with spaCy, NLTK, Transformers
- LLM prompt engineering
- Web scraping with BeautifulSoup/Scrapy
- Style mimicry and text generation
- Aphra agent definitions
```

#### Para P3 (Frontend Lead):
```
I'm building a Next.js 14 blog with App Router and Tailwind CSS.
Focus on:
- Next.js App Router patterns
- React Server Components
- Tailwind CSS styling
- TypeScript type safety
- Responsive design
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
```

### Agents (P2)
```txt
spacy>=3.7.0
nltk>=3.8.0
transformers>=4.35.0
beautifulsoup4>=4.12.0
scrapy>=2.11.0
openai>=1.3.0
anthropic>=0.7.0
langchain>=0.1.0
```

### Frontend (P3)
```json
{
  "next": "^14.0.0",
  "react": "^18.2.0",
  "tailwindcss": "^3.4.0"
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

---

## 🎯 Objetivos del Proyecto

1. **Análisis completo** del estilo de escritura de javipas.com
2. **Sistema multi-agente** funcional con Aphra
3. **Generación automática** de artículos que imiten el estilo
4. **Blog Next.js** con diseño similar al original
5. **Deployment funcional** en Modal
6. **Documentación completa** del TFG

---

**Última actualización**: 10 de febrero de 2026

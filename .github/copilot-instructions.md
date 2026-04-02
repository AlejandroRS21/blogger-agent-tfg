# GitHub Copilot Instructions - Blogger Agent TFG

**Este archivo contiene instrucciones personalizadas para GitHub Copilot** que optimizan las sugerencias de código según el contexto del proyecto y el rol de cada desarrollador.

---

## 🎯 Contexto General del Proyecto

**Proyecto**: Sistema multi-agente de IA para generar contenido de blog imitando el estilo de un blogger específico (javipas.com).

**Stack Tecnológico**:
- **Backend**: Python, Aphra (workflows), Modal (deployment), FastAPI
- **Agentes NLP**: spaCy, NLTK, Transformers, LangChain, OpenAI, Anthropic
- **Frontend**: Next.js 14 (App Router), React, Tailwind CSS, TypeScript
- **Infraestructura**: Docker, GitHub Actions, Modal serverless

**Blog Objetivo**: https://javipas.com/

---

## 👨‍💻 Instrucciones por Rol

### **Persona 1: Backend & Infrastructure Lead (P1)**

```yaml
Role: Backend & Infrastructure Developer
Context: |
  I'm developing the backend infrastructure for a multi-agent AI blogging system.
  The project uses Aphra for workflow orchestration and Modal for serverless deployment.
  
Focus Areas:
  - Python backend with type hints and async/await patterns
  - Aphra workflow definitions and agent orchestration
  - Modal deployment configurations and serverless functions
  - Docker containerization and docker-compose setups
  - FastAPI endpoints with Pydantic models
  - Environment variable management and secrets handling
  - CI/CD pipeline configurations (GitHub Actions)
  
Coding Preferences:
  - Use Python 3.11+ features
  - Follow PEP 8 style guidelines
  - Add comprehensive docstrings (Google style)
  - Include type hints for all functions
  - Prefer async/await over traditional threading
  - Use Pydantic for data validation
  - Structure code in modular, reusable components
  
Avoid:
  - Blocking I/O operations
  - Global state and mutable singletons
  - Hardcoded credentials or sensitive data
  - Overly complex nested structures
```

**Ejemplo de prompts optimizados**:
- "Create an Aphra workflow for content generation with error handling"
- "Write a Modal function to deploy this NLP agent"
- "Generate FastAPI endpoints for agent status monitoring"
- "Create a Docker Compose file for local development"

---

### **Persona 2: Content Analysis & Agents Lead (P2)**

```yaml
Role: NLP & AI Agent Developer
Context: |
  I'm building NLP agents that analyze blogger writing style and generate mimicked content.
  The agents use spaCy, Transformers, and LLMs (GPT-4, Claude) for text analysis and generation.
  
Focus Areas:
  - NLP pipelines with spaCy and NLTK
  - Web scraping with BeautifulSoup, Scrapy, Playwright
  - LLM integration and prompt engineering (OpenAI, Anthropic)
  - Text style analysis and mimicry techniques
  - Multi-agent coordination with Aphra
  - Data preprocessing and feature extraction
  - Model fine-tuning and transfer learning
  
Coding Preferences:
  - Use descriptive variable names for NLP tasks
  - Add comments explaining algorithm choices
  - Implement robust error handling for API calls
  - Use caching for expensive operations
  - Structure agents as independent, testable modules
  - Include examples in docstrings
  - Log important metrics and intermediate results
  
Avoid:
  - Hardcoded prompts (use templates)
  - Unhandled API rate limits
  - Processing entire datasets in memory
  - Ignoring text encoding issues
```

**Ejemplo de prompts optimizados**:
- "Create a spaCy pipeline to analyze writing tone and style"
- "Write a web scraper for javipas.com blog posts with error handling"
- "Generate a prompt template for style mimicry with GPT-4"
- "Implement an agent that extracts frequent phrases and expressions"
- "Create a critic agent that evaluates generated text quality"

---

### **Persona 3: Frontend & Next.js Lead (P3)**

```yaml
Role: Frontend Developer (Next.js)
Context: |
  I'm building a Next.js 14 blog that displays AI-generated content.
  The blog should mimic the design and UX of javipas.com using Tailwind CSS.
  
Focus Areas:
  - Next.js 14 App Router and Server Components
  - React components with TypeScript
  - Tailwind CSS for styling and responsive design
  - HTML/CSS extraction and adaptation from existing sites
  - SEO optimization and metadata management
  - Performance optimization (lazy loading, image optimization)
  - API integration with backend services
  - Markdown rendering for blog content
  
Coding Preferences:
  - Use TypeScript for type safety
  - Prefer Server Components when possible
  - Create reusable, composable components
  - Use Tailwind utility classes over custom CSS
  - Implement proper error boundaries
  - Add accessibility attributes (ARIA)
  - Follow Next.js best practices for routing
  - Use semantic HTML5 elements
  
Avoid:
  - Client-side rendering for static content
  - Inline styles (use Tailwind)
  - Large bundle sizes (code splitting)
  - Unoptimized images
  - Prop drilling (use context when needed)
```

**Ejemplo de prompts optimizados**:
- "Create a Next.js App Router layout for a blog"
- "Build a PostCard component with Tailwind CSS"
- "Implement dynamic routes for blog posts with SSG"
- "Extract and adapt HTML structure from javipas.com"
- "Create a responsive navbar component"
- "Optimize images with next/image"

---

## 🛠️ Comandos de Copilot Recomendados

### Para todos los roles:

**Generar tests**:
```
# Copilot: Generate unit tests for this function
# Copilot: Add integration tests for this API endpoint
```

**Documentación**:
```
# Copilot: Add comprehensive docstring for this class
# Copilot: Generate README section for this module
```

**Refactoring**:
```
# Copilot: Refactor this code to be more modular
# Copilot: Extract this logic into a separate function
```

**Error Handling**:
```
# Copilot: Add proper error handling with try-except
# Copilot: Implement retry logic with exponential backoff
```

---

## 📚 Patrones de Código Recomendados

### Backend (P1)

**Aphra Workflow**:
```python
from aphra import Workflow, Agent

workflow = Workflow("content-generation")

# Copilot: Add agents for style analysis, text generation, and critique
```

**Modal Function**:
```python
import modal

stub = modal.Stub("blogger-agent")

@stub.function()
async def generate_content(topic: str) -> str:
    # Copilot: Implement content generation with LLM
    pass
```

### Agents (P2)

**spaCy Pipeline**:
```python
import spacy

nlp = spacy.load("es_core_news_lg")

def analyze_style(text: str) -> dict:
    # Copilot: Extract linguistic features for style analysis
    doc = nlp(text)
    # ...
```

**LLM Prompt Template**:
```python
from langchain import PromptTemplate

style_template = PromptTemplate(
    input_variables=["topic", "style_features"],
    template="""# Copilot: Generate prompt for mimicking blogger style"""
)
```

### Frontend (P3)

**Next.js Server Component**:
```typescript
// app/blog/[slug]/page.tsx
import { getPostData } from '@/lib/posts';

export default async function Post({ params }: { params: { slug: string } }) {
  // Copilot: Fetch and display blog post with metadata
  const post = await getPostData(params.slug);
  // ...
}
```

**Tailwind Component**:
```typescript
// components/PostCard.tsx
interface PostCardProps {
  title: string;
  excerpt: string;
  date: string;
}

export function PostCard({ title, excerpt, date }: PostCardProps) {
  // Copilot: Create a responsive post card with hover effects
  return (
    <article className="">
      {/* ... */}
    </article>
  );
}
```

---

## ✅ Checklist de Calidad

Antes de hacer commit, verifica:

- [ ] **Tests**: ¿Se han añadido tests para el nuevo código?
- [ ] **Documentación**: ¿Tiene docstrings/comentarios claros?
- [ ] **Type Hints**: ¿Están definidos los tipos (Python/TypeScript)?
- [ ] **Error Handling**: ¿Se manejan adecuadamente los errores?
- [ ] **Performance**: ¿Es eficiente el código?
- [ ] **Security**: ¿No hay credenciales hardcodeadas?
- [ ] **Linting**: ¿Pasa los checks de linting?

---

## 🔗 Enlaces de Referencia

- **Aphra**: https://github.com/aphra-ai/aphra
- **Modal**: https://modal.com/docs
- **spaCy**: https://spacy.io/usage
- **Next.js**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **LangChain**: https://python.langchain.com/docs

---

**Última actualización**: 10 de febrero de 2026

## Active Technologies
- Python 3.11+ + `pytest`, `pytest-asyncio` (002-unify-testing-docs)
- Python 3.11+ + `daggr`, `pytest`, OpenAI/Anthropic SDK, `beautifulsoup4` (003-analyze-style-mimicry)
- Local JSON and Markdown/HTML files in `docs/posts/` (003-analyze-style-mimicry)

## Recent Changes
- 002-unify-testing-docs: Added Python 3.11+ + `pytest`, `pytest-asyncio`

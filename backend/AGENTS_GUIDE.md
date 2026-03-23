# Blogger Agent TFG - Documentación para Agentes IA

## 📋 Resumen del Proyecto

Sistema multi-agente que analiza el estilo de escritura de un blogger (Javi Pas - javipas.com) y genera artículos nuevos sobre temas actuales, imitando su estilo.

### Características principales:
- ✅ Extrae estilo de blogger (vocabulario, expresiones, tono)
- ✅ Busca noticias actuales sobre cualquier tema
- ✅ Genera artículos con el estilo del blogger
- ✅ Despliega automáticamente a GitHub Pages

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    Blogger Agent Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│  1. SCRAPER        → Extrae artículos del blogger         │
│  2. STYLE EXTRACTOR→ Analiza estilo (vocabulario, etc.)   │
│  3. NEWS RESEARCH  → Busca noticias actuales              │
│  4. CONTENT GEN    → Genera artículo con estilo            │
│  5. DEPLOY         → Despliega a GitHub Pages               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Archivos

```
backend/
├── aphra_blogger/
│   ├── agents/
│   │   ├── style_extractor.py     # Extrae perfil de estilo
│   │   ├── content_generator.py   # Genera artículos
│   │   ├── news_research_agent.py  # Busca noticias actuales
│   │   └── ...
│   └── llm/
│       ├── factory.py              # Factory de proveedores LLM
│       ├── gemini_provider.py      # Google Gemini
│       ├── huggingface_provider.py# HuggingFace
│       └── openai_provider.py      # OpenAI
├── tools/
│   └── scraper.py                  # Extrae artículos de blogs
├── generate_and_deploy.py          # Script principal
└── javipas_style_profile.json     # Perfil de estilo de Javi Pas
```

---

## 🚀 Cómo Usar el Sistema

### 1. Requisitos Previos

- Python 3.11+
- Token de API (Gemini, HuggingFace, u OpenAI)

### 2. Configuración

#### Opción A: Google Gemini (Recomendado - Gratis)
```bash
# Obtén tu token en: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="tu_token_aqui"
```

#### Opción B: HuggingFace (Gratis con límites)
```bash
# Obtén tu token en: https://huggingface.co/settings/tokens
export HF_TOKEN="tu_token_aqui"
```

#### Opción C: OpenAI (De pago)
```bash
export OPENAI_API_KEY="sk-tu_token_aqui"
```

### 3. Generar un Artículo

```bash
cd backend
python3 generate_and_deploy.py "Elon Musk y la IA en 2026"
```

El script te preguntará:
- **Tema del artículo**: "Elon Musk y la IA en 2026"
- **¿Desplegar a GitHub Pages?**: Responde "s" o "n"

### 4. Ver el Resultado

- **Blog en vivo**: https://alejandrors21.github.io/blogger-agent-tfg/
- **Posts**: https://alejandrors21.github.io/blogger-agent-tfg/posts/

---

## 🔧 Componentes del Sistema

### StyleExtractor
Extrae el perfil de estilo de un blogger:
- Vocabulario característico
- Expresiones típicas
- Temas que trata
- Tono y voz
- Cómo empieza/termina los artículos

**Archivo de perfil**: `javipas_style_profile.json`

### NewsResearchAgent
Busca noticias actuales sobre un tema:
- Soporta Brave Search, Exa, o fallback básico
- Extrae hallazgos clave
- Identifica temas relacionados

### ContentGenerator
Genera artículos con el estilo del blogger:
- Usa few-shot learning
- Incorpora vocabulario y expresiones del perfil
- Genera artículos de 1500-2500 palabras (con LLM)

---

## 📝 Ejemplos de Uso

### Generar artículo simple
```bash
python3 generate_and_deploy.py "Apple Intelligence 2026"
```

### Generar sin desplegar (para testing)
```bash
echo "n" | python3 generate_and_deploy.py "Tu tema"
```

### Usar con HuggingFace
```bash
HF_TOKEN="tu_token" python3 generate_and_deploy.py "Tu tema"
```

---

## 🔍 Topics Recomendados

Algunos temas que funcionan bien con el estilo de Javi Pas:

- "El futuro de la IA en móviles"
- "Apple vs Google: la guerra de la IA"
- "Tesla y los coches autónomos"
- "ChatGPT y la IA generativa"
- "Por qué los Macs con IA van a cambiar todo"
- "Las nuevas funciones de OpenAI"

---

## ⚠️ Notas Importantes

1. **Sin token API**: El sistema usa un fallback básico que genera artículos cortos (~300 palabras)
2. **Con token API**: Artículos completos de 1500-2500 palabras
3. **GitHub Pages**: El blog se actualiza automáticamente tras el deploy
4. **Estilo del blogger**: El sistema está configurado para imitar a Javi Pas (javipas.com)

---

## 📚 Archivos de Referencia

- `javipas_corpus.json` - Artículos extraídos de javipas.com
- `javipas_style_profile.json` - Perfil de estilo calculado
- `javipas_prompt_context.txt` - Contexto para prompts
- `docs/posts/` - Artículos generados (JSON)
- `docs/posts.json` - Índice de artículos

---

## 🤖 Para Agentes IA

Si eres un agente IA usando este repo:

1. **Configura tu API key** antes de generar contenido
2. **Usa generate_and_deploy.py** como punto de entrada principal
3. **El estilo está predefined** en `javipas_style_profile.json`
4. **No necesitas modificar el scraper** - el corpus ya está extraído
5. **Para temas diferentes**, simplemente cambia el argumento

### Ejemplo de uso programático:

```python
import json
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.news_research_agent import NewsResearchAgent

# Cargar perfil de estilo
with open('javipas_style_profile.json') as f:
    style = json.load(f)

# Buscar noticias
news = NewsResearchAgent()
news_result = news.research_and_format_for_generation("Tu tema")

# Generar contenido
gen = ContentGenerator()
gen.style_profile = style
content = gen.generate_draft("Tu tema", keywords=news_result['related_topics'])

print(content)
```

---

## 📞 Soporte

- **Repo**: https://github.com/AlejandroRS21/blogger-agent-tfg
- **Blog**: https://alejandrors21.github.io/blogger-agent-tfg/
- **Autor**: AlejandroRS21
- **Proyecto**: TFG - IES Rafael Alberti

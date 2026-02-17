"""
Blogger Agent TFG - Visualización Real del Flujo de Agentes con Daggr
====================================================================

Esta aplicación utiliza los agentes reales del backend para generar
posts de blog, visualizando cada paso en el grafo de Daggr.

Uso:
    uv run python daggr_blogger_workflow.py
    
Luego abrir: http://localhost:7860
"""

import os
import sys
import json
import gradio as gr
from daggr import FnNode, Graph
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno de forma robusta
backend_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(backend_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"✅ Variables de entorno cargadas desde {env_path}")
else:
    print(f"⚠️ No se encontró el archivo .env en {env_path}")

# Asegurar que el path del backend esté disponible
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.orchestrator.config import OrchestratorConfig
from aphra_blogger.llm.factory import create_llm_provider
from aphra_blogger.agents.style_analyzer import StyleAnalyzer
from aphra_blogger.agents.keyword_extractor import KeywordExtractor
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.critic import CriticAgent
from aphra_blogger.agents.image_selector import ImageSelectorAgent
from aphra_blogger.agents.html_builder import HTMLBuilder

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

class WorkflowState:
    def __init__(self):
        self.config = OrchestratorConfig.default()
        self.llm = None
        self.agents = {}

state = WorkflowState()

def initialize_agents(provider: str, api_key: str):
    if provider:
        state.config.provider = provider
    
    # Priorizar API key pasada por el usuario, si no usar la de .env
    actual_key = api_key if api_key and api_key.strip() != "" else None
    
    # Debug info
    print(f"Initializing agents with provider: {provider}")
    print(f"MODAL_TOKEN_ID present in env: {bool(os.getenv('MODAL_TOKEN_ID'))}")

    if provider == "modal":
        state.config.modal_api_key = actual_key or os.getenv("MODAL_TOKEN_ID")
    elif provider == "huggingface":
        state.config.hf_token = actual_key or os.getenv("HF_TOKEN")
        if actual_key: os.environ["HF_TOKEN"] = actual_key
    elif provider == "openai":
        state.config.openai_api_key = actual_key or os.getenv("OPENAI_API_KEY")
        if actual_key: os.environ["OPENAI_API_KEY"] = actual_key

    # Crear LLM
    try:
        state.llm = create_llm_provider(
            provider=state.config.provider,
            api_key=actual_key,
            temperature=state.config.temperature
        )
        
        # Crear Agentes usando el LLM ya inicializado
        state.agents = {
            "style": StyleAnalyzer(provider=state.config.provider, api_key=actual_key),
            "keywords": KeywordExtractor(provider=state.config.provider, api_key=actual_key),
            "generator": ContentGenerator(provider=state.config.provider, api_key=actual_key),
            "critic": CriticAgent(provider=state.config.provider, api_key=actual_key),
            "images": ImageSelectorAgent(provider=state.config.provider, api_key=actual_key),
            "html": HTMLBuilder(provider=state.config.provider, api_key=actual_key)
        }
        return f"✅ Agentes listos con {state.config.provider.upper()}"
    except Exception as e:
        return f"❌ Error al inicializar: {str(e)}"

# ============================================================================
# NODOS DEL GRAFO
# ============================================================================

def setup_workflow(provider: str, api_key: str) -> str:
    return initialize_agents(provider, api_key)

config_node = FnNode(
    fn=setup_workflow,
    name="⚙️ Configuración",
    inputs={
        "provider": gr.Dropdown(choices=["modal", "huggingface", "openai"], value="modal", label="Proveedor LLM"),
        "api_key": gr.Textbox(label="API Key / Token (Opcional si está en .env)", type="password")
    },
    outputs={"status": gr.Textbox(label="Estado")}
)

def ensure_agents():
    if not state.agents:
        res = initialize_agents("modal", "")
        if "❌" in res:
            raise Exception(res)

def analyze_style(status: str, blogger_name: str, sample_posts: str) -> str:
    ensure_agents()
    analysis = state.agents["style"].analyze(blogger_urls=[], sample_text=sample_posts)
    return json.dumps(analysis, indent=2, ensure_ascii=False)

style_analyzer = FnNode(
    fn=analyze_style,
    name="1️⃣ Style Analyzer",
    inputs={
        "status": config_node.status,
        "blogger_name": gr.Textbox(label="Blogger", value="TechGuru"),
        "sample_posts": gr.Textbox(label="Muestras de estilo", lines=5, value="Hoy aprendí sobre React Hooks.\nLa IA está cambiando el mundo.")
    },
    outputs={"style_json": gr.Textbox(label="Análisis de Estilo", lines=10)}
)

def extract_keywords(topic: str, style_json: str) -> Dict[str, str]:
    ensure_agents()
    style = json.loads(style_json)
    res = state.agents["keywords"].extract(blogger_urls=[], sample_text=topic)
    keywords = res.get("keywords", [])
    return {"keywords": ", ".join(keywords), "topic": topic}

keyword_extractor = FnNode(
    fn=extract_keywords,
    name="2️⃣ Keyword Extractor",
    inputs={
        "topic": gr.Textbox(label="Tema del Post", value="El futuro de Next.js"),
        "style_json": style_analyzer.style_json
    },
    outputs={
        "keywords": gr.Textbox(label="Keywords Extraídas"),
        "topic": gr.State()
    }
)

def generate_content(topic: str, keywords: str, style_json: str) -> str:
    ensure_agents()
    style = json.loads(style_json)
    kw_list = [k.strip() for k in keywords.split(",")]
    content = state.agents["generator"].generate_draft(topic=topic, style_profile=style, keywords=kw_list)
    return content

content_generator = FnNode(
    fn=generate_content,
    name="3️⃣ Content Generator",
    inputs={
        "topic": keyword_extractor.topic,
        "keywords": keyword_extractor.keywords,
        "style_json": style_analyzer.style_json
    },
    outputs={"draft_content": gr.Markdown(label="Borrador")}
)

def critique_content(topic: str, content: str, style_json: str) -> str:
    ensure_agents()
    style = json.loads(style_json)
    critique = state.agents["critic"].critique(content=content, style_profile=style, topic=topic)
    return json.dumps(critique, indent=2, ensure_ascii=False)

critic_agent = FnNode(
    fn=critique_content,
    name="4️⃣ Critic Agent",
    inputs={
        "topic": keyword_extractor.topic,
        "content": content_generator.draft_content,
        "style_json": style_analyzer.style_json
    },
    outputs={"critique_json": gr.Textbox(label="Crítica", lines=10)}
)

def select_images(topic: str, content: str) -> str:
    ensure_agents()
    images = state.agents["images"].select_images(content=content, topic=topic)
    return json.dumps(images, indent=2)

image_selector = FnNode(
    fn=select_images,
    name="5️⃣ Image Selector",
    inputs={
        "topic": keyword_extractor.topic,
        "content": content_generator.draft_content
    },
    outputs={"image_urls": gr.Textbox(label="Imágenes")}
)

def build_html(topic: str, content: str, images_json: str, style_json: str) -> str:
    ensure_agents()
    style = json.loads(style_json)
    images = json.loads(images_json)
    output = state.agents["html"].build(content=content, topic=topic, images=images, style_profile=style)
    
    # NUEVO: Guardar el post para el frontend
    try:
        slug = topic.lower().replace(" ", "-").replace("?", "").replace("!", "")
        # Aseguramos que existe el directorio
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "posts")
        os.makedirs(output_dir, exist_ok=True)
        
        post_data = {
            "id": slug,
            "title": topic,
            "description": content[:150] + "...",
            "html_code": output.html,
            "metadata": {
                "word_count": len(content.split()),
                "reading_time": max(1, len(content.split()) // 200),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "author": "Blogger Agent",
                "tags": style.get("personality_traits", ["AI"])
            }
        }
        
        # Guardar archivo individual
        with open(os.path.join(output_dir, f"{slug}.json"), "w", encoding="utf-8") as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Post guardado en: {output_dir}/{slug}.json")
    except Exception as e:
        print(f"⚠️ Error al guardar el post: {e}")

    return output.html

html_builder = FnNode(
    fn=build_html,
    name="6️⃣ HTML Builder",
    inputs={
        "topic": keyword_extractor.topic,
        "content": content_generator.draft_content,
        "images_json": image_selector.image_urls,
        "style_json": style_analyzer.style_json
    },
    outputs={"final_html": gr.HTML(label="🎉 Post Final")}
)

# ============================================================================
# LANZAMIENTO
# ============================================================================

graph = Graph(
    name="🚀 Blogger Agent TFG - LIVE Workflow",
    nodes=[config_node, style_analyzer, keyword_extractor, content_generator, critic_agent, image_selector, html_builder],
)

if __name__ == "__main__":
    print("-" * 50)
    print("Lanzando Daggr con agentes reales del backend...")
    print("Abriendo en http://localhost:7860")
    print("-" * 50)
    graph.launch(share=False)

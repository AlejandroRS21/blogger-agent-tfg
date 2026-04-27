"""
Blogger Agent TFG — HuggingFace Spaces (Daggr + Gradio)
=========================================================
Interfaz visual para generar posts llamando al orquestador en Modal.

Deploy en HF Spaces:
    1. Crear Space en huggingface.co/spaces (Gradio SDK)
    2. Subir hf_spaces/ al repo del Space
    3. Configurar secrets: MODAL_WEBHOOK_URL

Arquitectura:
    HF Spaces (UI) ──POST──► Modal (Orquestador + Qwen 2.5) ──► GitHub (post JSON) ──► Vercel (blog)
"""

import os
import json
import time
import requests
import gradio as gr
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
MODAL_WEBHOOK_URL = os.getenv(
    "MODAL_WEBHOOK_URL",
    "https://alejandrors21--blogger-agent-tfg-webhook.modal.run"
)
MODAL_CONTINUOUS_URL = os.getenv(
    "MODAL_CONTINUOUS_URL", 
    "https://alejandrors21--blogger-agent-tfg-continuous-webhook.modal.run"
)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "IES-Rafael-Alberti/blogger-agent-tfg")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

# ── Theme ──────────────────────────────────────────────────────
theme = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="slate",
    font=gr.themes.GoogleFont("Inter"),
).set(
    body_background_fill="*neutral_50",
    block_background_fill="white",
    block_border_width="1px",
    block_border_color="*neutral_200",
)


def generate_post(
    topic: str,
    blog_url: str,
    provider: str,
    min_words: int,
    max_words: int,
) -> tuple:
    """Call Modal webhook to generate a blog post."""
    
    if not topic.strip():
        return "⚠️ Ingresá un tema para generar el post.", "", ""
    
    payload = {
        "blogger_urls": [blog_url],
        "topic": topic.strip(),
        "enable_critique": True,
        "min_word_count": min_words,
        "max_word_count": max_words,
        "provider": provider,
    }
    
    start = time.time()
    
    try:
        resp = requests.post(
            MODAL_WEBHOOK_URL,
            json=payload,
            timeout=300,
        )
        elapsed = time.time() - start
        
        if resp.status_code != 200:
            return f"❌ Error {resp.status_code}: {resp.text}", "", ""
        
        data = resp.json()
        
        if not data.get("success"):
            return f"❌ Error: {data.get('error', 'Unknown')}", "", ""
        
        result = data["data"]
        
        # Extract info
        content = result.get("content", "")
        style = result.get("style_profile", {})
        keywords = result.get("keywords", [])
        html_data = result.get("html_structure", {})
        
        # Build markdown summary
        summary = f"""## ✅ Post Generado — {elapsed:.1f}s

### 📊 Métricas
- **Palabras**: {html_data.get('word_count', len(content.split()))}
- **Tiempo de lectura**: {html_data.get('reading_time', '?')} min
- **Keywords**: {', '.join(keywords[:10]) if keywords else 'N/A'}

### 🎨 Estilo Detectado
- **Tono**: {style.get('tone', 'N/A')}
- **Voz**: {style.get('voice', 'N/A')}

### 🖼️ Imágenes
{_format_images(result.get('images', []))}

---
*Generado con Qwen 2.5 7B en Modal · {datetime.now().strftime('%H:%M')}*
"""
        
        # Post JSON for saving
        post_json = {
            "slug": _slugify(topic),
            "title": html_data.get("meta_title", topic),
            "date": datetime.now().isoformat(),
            "excerpt": html_data.get("meta_description", content[:200]),
            "content": content,
            "tags": keywords[:8] if keywords else [],
            "image": _first_image(result.get("images", [])),
            "author": "Blogger Agent",
            "meta": {
                "reading_time": html_data.get("reading_time", 5),
                "word_count": html_data.get("word_count", 0),
                "keywords": keywords,
            }
        }
        
        return summary, content, json.dumps(post_json, indent=2, ensure_ascii=False)
        
    except requests.exceptions.Timeout:
        return "⏱️ Timeout: Modal tardó más de 5 min. ¿Está en cold start?", "", ""
    except Exception as e:
        return f"❌ Error: {str(e)}", "", ""


def save_to_github(post_json_str: str, topic: str) -> str:
    """Save generated post to GitHub repo (triggers Vercel deploy)."""
    
    if not post_json_str or not GITHUB_TOKEN:
        return "⚠️ Configurá GITHUB_TOKEN en los secrets del Space para guardar posts."
    
    try:
        post_data = json.loads(post_json_str)
        slug = post_data.get("slug", _slugify(topic))
        
        # 1. Update posts.json catalog
        catalog_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/docs/posts.json"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        # Get current catalog
        resp = requests.get(catalog_url, headers=headers)
        if resp.status_code == 200:
            current = json.loads(resp.json().get("content", "[]"))
            sha = resp.json().get("sha", "")
        else:
            current = []
            sha = ""
        
        # Add new post to catalog
        catalog_entry = {
            "slug": slug,
            "title": post_data["title"],
            "date": post_data["date"],
            "excerpt": post_data.get("excerpt", ""),
            "tags": post_data.get("tags", []),
            "image": post_data.get("image", ""),
            "author": post_data.get("author", "Blogger Agent"),
        }
        
        # Remove existing entry if same slug
        current = [p for p in current if isinstance(p, dict) and p.get("slug") != slug]
        current.insert(0, catalog_entry)
        
        # Update catalog
        requests.put(
            catalog_url,
            headers=headers,
            json={
                "message": f"📝 Nuevo post: {post_data['title'][:50]}",
                "content": json.dumps(current, indent=2, ensure_ascii=False),
                "sha": sha,
                "branch": GITHUB_BRANCH,
            },
        )
        
        # 2. Save individual post file
        post_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/docs/posts/{slug}.json"
        
        # Check if exists
        resp = requests.get(post_url, headers=headers)
        post_sha = resp.json().get("sha", "") if resp.status_code == 200 else ""
        
        requests.put(
            post_url,
            headers=headers,
            json={
                "message": f"📝 Post: {post_data['title'][:50]}",
                "content": json.dumps(post_data, indent=2, ensure_ascii=False),
                "sha": post_sha,
                "branch": GITHUB_BRANCH,
            },
        )
        
        return f"✅ Post guardado en GitHub → Vercel se desplegará automáticamente\n📄 `docs/posts/{slug}.json`"
        
    except Exception as e:
        return f"❌ Error guardando en GitHub: {str(e)}"


def continuous_generate(topic_list: str, blog_url: str, cycles: int) -> str:
    """Run continuous publishing via Modal."""
    if not topic_list.strip():
        return "⚠️ Ingresá al menos un tema."
    
    topics = [t.strip() for t in topic_list.split("\n") if t.strip()]
    
    payload = {
        "blogger_urls": [blog_url],
        "topic_candidates": [{"topic": t} for t in topics],
        "cycles": cycles,
        "provider": "auto",
    }
    
    try:
        resp = requests.post(MODAL_CONTINUOUS_URL, json=payload, timeout=600)
        data = resp.json()
        
        if data.get("success"):
            result = data["data"]
            posts_count = len(result.get("generated_posts", []))
            return f"✅ Publicación continua completada: {posts_count} posts en {cycles} ciclos"
        else:
            return f"❌ Error: {data.get('error')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ── Helpers ────────────────────────────────────────────────────
def _slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:80]


def _format_images(images: list) -> str:
    if not images:
        return "N/A"
    lines = []
    for i, img in enumerate(images[:5], 1):
        pos = img.get("position", "?")
        prompt = img.get("prompt", "")[:100]
        lines.append(f"{i}. **[{pos}]** {prompt}...")
    return "\n".join(lines)


def _first_image(images: list) -> str:
    if images and images[0].get("prompt"):
        return images[0]["prompt"][:200]
    return ""


# ── Gradio UI ──────────────────────────────────────────────────
with gr.Blocks(theme=theme, title="Blogger Agent TFG", css="""
    .generated-content { max-height: 500px; overflow-y: auto; }
    .gr-button-primary { background: linear-gradient(135deg, #dc2626, #ea580c) !important; }
""") as demo:

    gr.Markdown("""
    # 🤖 Blogger Agent TFG
    
    Generá posts que imitan el estilo de [JaviPas](https://javipas.com) usando **Qwen 2.5 7B** en Modal.
    
    Arquitectura: `HF Spaces → Modal (Qwen 2.5) → GitHub → Vercel`
    """)

    with gr.Tabs():
        # ── Single Post Generation ──
        with gr.Tab("📝 Generar Post"):
            with gr.Row():
                with gr.Column(scale=1):
                    topic = gr.Textbox(
                        label="Tema del post",
                        placeholder="Ej: El futuro de la IA en educación",
                        lines=2,
                    )
                    blog_url = gr.Textbox(
                        label="Blog de referencia",
                        value="https://javipas.com",
                    )
                    provider = gr.Dropdown(
                        label="Provider LLM",
                        choices=["auto", "vllm", "huggingface"],
                        value="auto",
                    )
                    with gr.Row():
                        min_words = gr.Slider(400, 1500, value=800, step=100, label="Mín. palabras")
                        max_words = gr.Slider(1000, 4000, value=2500, step=100, label="Máx. palabras")

                    gen_btn = gr.Button("🚀 Generar Post", variant="primary", size="lg")
                    
                    gr.Markdown("---")
                    gr.Markdown("### 💾 Guardar en GitHub")
                    save_btn = gr.Button("📤 Guardar post → Vercel", variant="secondary")
                    save_status = gr.Textbox(label="Estado", interactive=False)

                with gr.Column(scale=2):
                    summary = gr.Markdown("Esperando tema...", elem_classes="generated-content")
                    post_json = gr.State(value="")

            gen_btn.click(
                fn=generate_post,
                inputs=[topic, blog_url, provider, min_words, max_words],
                outputs=[summary, gr.Textbox(visible=False), post_json],
            )

            save_btn.click(
                fn=save_to_github,
                inputs=[post_json, topic],
                outputs=[save_status],
            )

        # ── Continuous Publishing ──
        with gr.Tab("🔄 Publicación Continua"):
            gr.Markdown("""
            Generá múltiples posts en lote. Ideal para poblar el blog rápidamente.
            """)
            
            cont_topics = gr.Textbox(
                label="Temas (uno por línea)",
                placeholder="La revolución de los LLMs open-source\nPor qué Qwen supera a Llama en español\n...",
                lines=6,
            )
            cont_blog = gr.Textbox(label="Blog de referencia", value="https://javipas.com")
            cont_cycles = gr.Slider(1, 5, value=2, step=1, label="Ciclos de generación")

            cont_btn = gr.Button("🔄 Iniciar Publicación Continua", variant="primary")
            cont_status = gr.Textbox(label="Resultado", interactive=False)

            cont_btn.click(
                fn=continuous_generate,
                inputs=[cont_topics, cont_blog, cont_cycles],
                outputs=[cont_status],
            )

        # ── Info ──
        with gr.Tab("ℹ️ Arquitectura"):
            gr.Markdown("""
            ## 🏗️ Arquitectura del Sistema
            
            ```
            ┌─────────────────────┐
            │  HF Spaces (Gradio) │  ← Estás aquí
            │  Interfaz visual     │
            └────────┬────────────┘
                     │ POST /webhook
                     ▼
            ┌─────────────────────┐
            │  Modal (A10G GPU)   │
            │  Qwen 2.5 7B + vLLM │
            │  6 agentes IA        │
            └────────┬────────────┘
                     │ JSON post
                     ▼
            ┌─────────────────────┐
            │  GitHub Repo         │
            │  docs/posts/*.json   │
            └────────┬────────────┘
                     │ git push trigger
                     ▼
            ┌─────────────────────┐
            │  Vercel (Next.js)    │
            │  Blog estático       │
            │  javipas-agent.vercel│
            └─────────────────────┘
            ```
            
            ### 🔑 Secrets necesarios en HF Spaces
            - `MODAL_WEBHOOK_URL`: endpoint de Modal
            - `GITHUB_TOKEN`: token con permisos repo (para guardar posts)
            - `GITHUB_REPO`: `IES-Rafael-Alberti/blogger-agent-tfg`
            
            ### 💰 Costes
            - **Modal A10G**: ~$1.10/hr → ~$0.055/post
            - **HF Spaces**: Gratis (CPU básica)
            - **Vercel**: Gratis (plan hobby)
            - **GitHub**: Gratis
            """)

if __name__ == "__main__":
    demo.queue(max_size=5).launch(server_name="0.0.0.0", server_port=7860)

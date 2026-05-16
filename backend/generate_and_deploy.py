"""
Script para generar artículos sobre temas actuales y desplegarlos a GitHub Pages.

Uso:
    python generate_and_deploy.py "Tema del artículo"

Este script:
1. Investiga noticias sobre el tema
2. Genera artículo con estilo de Javi Pas
3. Guarda en docs/posts/
4. Actualiza docs/posts.json
5. Despliega a GitHub Pages
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aphra_blogger.agents.news_research_agent import NewsResearchAgent
from aphra_blogger.agents.content_generator import ContentGenerator
from aphra_blogger.agents.style_extractor import StyleExtractor


def generate_article(topic: str) -> dict:
    """Genera un artículo sobre un tema."""
    print(f"\n📰 Investigando: {topic}")

    # Cargar perfil de estilo
    style_profile = None
    if os.path.exists("javipas_style_profile.json"):
        with open("javipas_style_profile.json", "r", encoding="utf-8") as f:
            style_profile = json.load(f)

    # Investigar noticias
    news_agent = NewsResearchAgent()
    news_result = news_agent.research_and_format_for_generation(topic)

    # Generar contenido
    print(f"✍️ Generando artículo...")

    content_gen = ContentGenerator()
    content_gen.style_profile = style_profile or {}

    content = content_gen.generate_draft(
        topic=topic,
        keywords=news_result.get("related_topics", [])[:10],
        blogger_urls=None,
    )

    word_count = len(content.split())

    # Crear slug
    slug = topic.lower().replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    slug = slug[:60]

    # Estructura del post
    post = {
        "id": slug,
        "title": topic,
        "description": f"Artículo sobre {topic} generado con IA",
        "content": content,
        "html_code": f"<article>\n{content}\n</article>",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "author": style_profile.get("alias", "JaviPas") if style_profile else "IA Blogger",
        "word_count": word_count,
        "reading_time": max(1, word_count // 200),
        "tags": news_result.get("related_topics", [])[:5],
        "sources": [a["title"] for a in news_result.get("articles", [])[:3]],
        "generated_by": "AI Blogger Agent",
        "style_profile": style_profile.get("alias", "Unknown") if style_profile else "Unknown",
    }

    return post


def save_post(post: dict):
    """Guarda el post en docs/posts/"""
    # Ir a la raíz del proyecto
    project_root = Path(__file__).parent.parent
    docs_path = project_root / "docs" / "posts"
    docs_path.mkdir(parents=True, exist_ok=True)

    # Guardar post individual como HTML
    filename = docs_path / f"{post['id']}.html"
    with open(filename, "w", encoding="utf-8") as f:
        # Extraer el html del json provisto. Si no lo hay, crear dump simple
        html_code = post.get("html_code", f"<article>{post.get('content', '')}</article>")
        f.write(html_code)

    print(f"✓ Guardado en {filename}")
    return filename


def update_posts_index(new_post: dict):
    """Actualiza el índice de posts"""
    project_root = Path(__file__).parent.parent
    index_file = project_root / "docs" / "posts.json"

    # Cargar índice existente (es un array)
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            posts_index = json.load(f)
    else:
        posts_index = []

    # Añadir nuevo post
    post_summary = {
        "id": new_post["id"],
        "title": new_post["title"],
        "description": new_post["description"],
        "date": new_post["date"],
        "author": new_post["author"],
        "word_count": new_post["word_count"],
        "reading_time": new_post["reading_time"],
        "tags": new_post["tags"],
    }

    # Insertar al principio (posts_index es una lista)
    posts_index.insert(0, post_summary)

    # Guardar
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(posts_index, f, ensure_ascii=False, indent=2)

    print(f"✓ Índice actualizado en {index_file}")


def deploy_to_github():
    """Despliega a GitHub Pages"""
    print("\n🚀 Desplegando a GitHub Pages...")

    try:
        project_root = Path(__file__).parent.parent
        
        # Commit de los cambios nuevos
        subprocess.run(["git", "add", "docs/"], capture_output=True, cwd=project_root)
        subprocess.run(["git", "commit", "-m", "Deploy automático de nuevo post"], capture_output=True, cwd=project_root)

        # Eliminar rama local por si acaso
        subprocess.run(["git", "branch", "-D", "feature/github-pages-static"], capture_output=True, cwd=project_root)

        # Push directo (no subtree) hacia la rama de despliegue
        result = subprocess.run(
            ["git", "push", "origin", "HEAD:feature/github-pages-static", "--force"],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        if result.returncode == 0:
            print("✓ Despliegue completado!")
            print("📍 URL: https://alejandrors21.github.io/blogger-agent-tfg/")
        else:
            print(f"⚠️ Warning: {result.stderr}")
            print("✓ Pero el contenido se subió")

    except Exception as e:
        print(f"⚠️ Error en despliegue: {e}")


def main():
    if len(sys.argv) < 2:
        print('Uso: python generate_and_deploy.py "Tema del artículo"')
        print('Ejemplo: python generate_and_deploy.py "El futuro de la IA"')
        sys.exit(1)

    topic = sys.argv[1]

    print("=" * 60)
    print("GENERADOR DE ARTÍCULOS + DESPLIEGUE")
    print("=" * 60)
    print(f"\nTema: {topic}")

    # Generar artículo
    post = generate_article(topic)

    # Guardar
    save_post(post)
    update_posts_index(post)

    # Mostrar resultado
    print(f"\n📝 Artículo generado:")
    print(f"   - Palabras: {post['word_count']}")
    print(f"   - Autor: {post['author']}")
    print(f"   - Fecha: {post['date']}")
    print(f"   - Tags: {post['tags']}")

    # Preguntar si desplegar
    print("\n" + "=" * 60)
    deploy = input("¿Desplegar a GitHub Pages? (s/n): ").strip().lower()

    if deploy == "s" or deploy == "si" or deploy == "y" or deploy == "yes":
        deploy_to_github()
    else:
        print("OK. Para desplegar más tarde:")
        print("  powershell -ExecutionPolicy Bypass -File deploy.ps1")


if __name__ == "__main__":
    main()

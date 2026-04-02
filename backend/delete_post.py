import os
import sys
import json
import subprocess

if len(sys.argv) < 2:
    print("Uso: python backend/delete_post.py <id-del-post>")
    print("Ejemplo: python backend/delete_post.py avances-en-la-computacion-cuantica-2026")
    sys.exit(1)

post_id = sys.argv[1].strip()

docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
posts_dir = os.path.join(docs_dir, "posts")
json_path = os.path.join(docs_dir, "posts.json")

# 1. Eliminar archivo HTML
html_path = os.path.join(posts_dir, f"{post_id}.html")
if os.path.exists(html_path):
    os.remove(html_path)
    print(f"✅ Archivo eliminado: {html_path}")
else:
    print(f"⚠️ No se encontró el archivo: {html_path}")

# 2. Eliminar del JSON
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    new_posts = [p for p in posts if p.get("id") != post_id]
    
    if len(new_posts) < len(posts):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_posts, f, ensure_ascii=False, indent=2)
        print(f"✅ Post eliminado de posts.json")
    else:
        print(f"⚠️ El post con ID '{post_id}' no estaba en posts.json")

# 3. Empujar a GitHub automáticamente (opcional)
push = input("\n¿Deseas subir estos cambios a GitHub Pages ahora mismo para borrarlo de la web? (s/n): ")
if push.lower() == 's':
    project_root = os.path.join(os.path.dirname(__file__), "..")
    print("\nEmpujando a GitHub...")
    subprocess.run(["git", "add", "docs/"], cwd=project_root)
    subprocess.run(["git", "commit", "-m", f"Delete post {post_id}"], cwd=project_root)
    subprocess.run(["git", "push", "origin", "HEAD:feature/github-pages-static"], cwd=project_root)
    print("🚀 ¡Post eliminado correctamente de la web pública!")

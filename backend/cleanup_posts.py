import os
import json
import re
import unicodedata

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

docs_dir = "/media/arami/Antiguo disco del msi hdd/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/docs"
posts_dir = os.path.join(docs_dir, "posts")
json_path = os.path.join(docs_dir, "posts.json")

if not os.path.exists(json_path):
    print("No posts.json found")
    exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

unique_posts = {}
# Vamos a recorrer la lista de posts y limpiarla
for post in reversed(posts): # Empezamos por el final para quedarnos con el último duplicado
    old_id = post["id"]
    new_id = slugify(post["title"])
    post["id"] = new_id
    
    if new_id not in unique_posts:
        unique_posts[new_id] = post
    
    # Intentar renombrar/arreglar archivos
    old_html = os.path.join(posts_dir, f"{old_id}.html")
    old_json = os.path.join(posts_dir, f"{old_id}.json")
    new_html = os.path.join(posts_dir, f"{new_id}.html")
    
    # Solo tocamos si el nuevo path no existe o estamos arreglando archivos
    if os.path.exists(old_html) and old_html != new_html:
        print(f"Renaming {old_html} to {new_html}")
        os.rename(old_html, new_html)
    elif os.path.exists(old_json):
        # El archivo estaba en json! Vamos a extraer su HTML o simplemente copiar el contenido si es que tiene html_code
        try:
            with open(old_json, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                if 'html_code' in data:
                    print(f"Converting {old_json} to {new_html}")
                    with open(new_html, 'w', encoding='utf-8') as hf:
                        hf.write(data['html_code'])
                    os.remove(old_json)
                else:
                    print(f"Skipping {old_json}, does not have html_code")
        except json.JSONDecodeError:
            pass
            
# Archivos JSON sueltos que no estén en posts.json
for file in os.listdir(posts_dir):
    if file.endswith('.json'):
        filepath = os.path.join(posts_dir, file)
        try:
            with open(filepath, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                if 'html_code' in data and 'metadata' in data:
                    new_id = slugify(data['metadata']['title'])
                    new_html = os.path.join(posts_dir, f"{new_id}.html")
                    print(f"Converting orphaned {filepath} to {new_html}")
                    with open(new_html, 'w', encoding='utf-8') as hf:
                        hf.write(data['html_code'])
                    os.remove(filepath)
        except Exception as e:
            print(f"Error checking {filepath}: {e}")

# Save the deduplicated and fixed posts.json
final_posts = list(unique_posts.values())
# Sort by date descending
final_posts.sort(key=lambda x: x.get('date', ''), reverse=True)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(final_posts, f, ensure_ascii=False, indent=2)
    
print("Cleanup finished!")

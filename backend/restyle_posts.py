import os
import re
import markdown

docs_dir = "/media/arami/Antiguo disco del msi hdd/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/docs"
posts_dir = os.path.join(docs_dir, "posts")

# Template with Tailwind CSS
template = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title} - Blogger Agent IA</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Lora:ital@0;1&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .font-serif {{ font-family: 'Lora', serif; }}
    </style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    <!-- Header -->
    <header class="bg-white border-b sticky top-0 z-50">
        <nav class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <a href="../index.html" class="text-2xl font-black text-gray-900 tracking-tighter">BLOGGER<span class="text-blue-600">IA</span></a>
            <div class="flex gap-6 text-sm font-bold uppercase tracking-widest text-gray-400">
                <a href="../index.html" class="hover:text-blue-600 transition-colors">Volver al Blog</a>
            </div>
        </nav>
    </header>

    <main class="flex-grow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article class="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 md:p-12 overflow-hidden">
            <header class="mb-10 text-center border-b pb-10">
                <h1 class="text-4xl md:text-5xl font-black text-gray-900 tracking-tighter mb-4 leading-tight">{meta_title}</h1>
                <div class="flex items-center justify-center gap-3 text-sm font-bold uppercase tracking-widest text-gray-400">
                    <span>{reading_time} min de lectura</span>
                    <span class="bg-gray-200 w-1.5 h-1.5 rounded-full"></span>
                    <span>{word_count} palabras</span>
                </div>
            </header>
            
            <div class="prose prose-lg md:prose-xl max-w-none prose-a:text-blue-600 hover:prose-a:text-blue-500 font-serif prose-headings:font-sans prose-headings:font-black prose-img:rounded-2xl prose-img:shadow-md">
                {html_content}
            </div>
        </article>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t py-12 mt-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p class="text-xs font-black text-gray-400 uppercase tracking-widest leading-loose">
                © 2026 Blogger Agent TFG<br>
                AlejandroRS21 - Universidad San Pablo CEU
            </p>
        </div>
    </footer>
</body>
</html>'''

for file in os.listdir(posts_dir):
    if file.endswith('.html'):
        filepath = os.path.join(posts_dir, file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if it was already updated
        if 'cdn.tailwindcss.com' in content:
            continue
            
        print(f"Retro-styling {file}...")
        
        # Strip the wrapping <article></article> if they exist
        raw_md = re.sub(r'<article.*?>|</article>', '', content, flags=re.IGNORECASE | re.DOTALL).strip()
        
        # Find title
        title_match = re.search(r'^\s*#\s+(.+)$', raw_md, re.MULTILINE)
        if title_match:
            meta_title = title_match.group(1).strip()
            # Remove title from body to avoid duplication since it's already in the header
            raw_md = raw_md.replace(title_match.group(0), "", 1).strip()
        else:
            meta_title = "Artículo del Blog"

        # Calculate metrics
        word_count = len(raw_md.split())
        reading_time = max(1, word_count // 200)

        # Convert to HTML
        html_content = markdown.markdown(raw_md, extensions=['fenced_code', 'tables', 'nl2br'])

        new_html = template.format(
            meta_title=meta_title,
            reading_time=reading_time,
            word_count=word_count,
            html_content=html_content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)

print("Restyling completed successfully!")

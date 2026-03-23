# Guía de Publicación - Blogger Agent TFG

## 📖 Flujo Completo de Publicación

Este documento explica cómo se publican los artículos generados en el blog.

---

## 🔄 Flujo Automatizado (Recomendado)

### Opción 1: generate_and_deploy.py

```bash
cd backend
python3 generate_and_deploy.py "Tu tema aquí"
```

**Paso a paso:**
1. El script investiga noticias sobre el tema
2. Genera el artículo con estilo de Javi Pas
3. Guarda en `docs/posts/[slug].json`
4. Actualiza `docs/posts.json`
5. **Te pregunta**: "¿Desplegar a GitHub Pages?"
6. Responde **"s"** para hacer deploy automático

---

## 🔄 Flujo Manual (Para entender cómo funciona)

### Paso 1: Generar el artículo

```bash
cd backend
python3 -c "
from generate_and_deploy import generate_article, save_post, update_posts_index
post = generate_article('Tu tema aquí')
save_post(post)
update_posts_index(post)
"
```

### Paso 2: Hacer commit

```bash
git add docs/
git commit -m 'feat: nuevo artículo sobre [tema]'
```

### Paso 3: Desplegar a GitHub Pages

```bash
git subtree push --prefix docs origin gh-pages
```

---

## 📁 Archivos Involucrados

### 1. Artículos individuales
```
docs/posts/[slug].json
```
Ejemplo: `docs/posts/elon-musk-y-la-ia.json`

Estructura:
```json
{
  "id": "elon-musk-y-la-ia",
  "title": "Elon Musk y la IA",
  "content": "...",
  "date": "2026-03-23",
  "author": "JaviPas",
  "word_count": 1500,
  "tags": ["IA", "Tesla"]
}
```

### 2. Índice de artículos
```
docs/posts.json
```

Estructura:
```json
[
  {
    "id": "elon-musk-y-la-ia",
    "title": "Elon Musk y la IA",
    "date": "2026-03-23"
  },
  ...
]
```

---

## 🌐 GitHub Pages

### Rama gh-pages
El blog se sirve desde la rama `gh-pages` del repositorio.

### URL del blog
```
https://alejandrors21.github.io/blogger-agent-tfg/
```

### Actualización automática
Cada vez que se hace `git subtree push --prefix docs origin gh-pages`, el blog se actualiza automáticamente.

---

## ⚡ Comandos Rápidos

| Acción | Comando |
|--------|---------|
| Generar y deploy automático | `python3 generate_and_deploy.py "Tema"` |
| Solo generar (sin deploy) | `echo "n" \| python3 generate_and_deploy.py "Tema"` |
| Deploy manual | `git subtree push --prefix docs origin gh-pages` |
| Ver posts publicados | `cat docs/posts.json` |

---

## 🔧 Troubleshooting

### "Necesitas ejecutar desde el nivel superior"
```
cd /ruta/al/proyecto
git subtree push --prefix docs origin gh-pages
```

### El artículo no aparece
1. Verifica que se generó: `ls docs/posts/`
2. Verifica el índice: `cat docs/posts.json`
3. Haz commit: `git add docs/ && git commit -m "..."`
4. Despliega: `git subtree push --prefix docs origin gh-pages`

### Error de autenticación
Asegúrate de tener permisos de push al repo:
```bash
git push origin main
```

---

## 📋 Checklist para Publicar

- [ ] Artículo generado correctamente
- [ ] Guardado en `docs/posts/`
- [ ] Índice actualizado en `docs/posts.json`
- [ ] Commit hecho: `git add docs/ && git commit -m "..."`
- [ ] Deploy exitoso: `git subtree push --prefix docs origin gh-pages`
- [ ] Verificar en https://alejandrors21.github.io/blogger-agent-tfg/

---

## 🤖 Para Agentes IA

Si necesitas publicar un artículo:

1. **Genera el contenido** usando `generate_and_deploy.py`
2. **Responde "s"** cuando pregunte por deploy
3. **El script hace todo**: commit + deploy automático

Si prefieres hacerlo manualmente:
1. Genera el artículo
2. `git add docs/`
3. `git commit -m "feat: nuevo artículo"`
4. `git subtree push --prefix docs origin gh-pages`

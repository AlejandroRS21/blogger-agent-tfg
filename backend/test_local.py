#!/usr/bin/env python3
"""
test_local.py — Diagnóstico local del sistema Blogger Agent TFG
================================================================
Prueba secuencialmente:
  1. Variables de entorno y configuración
  2. Proveedor LLM (Gemini → HuggingFace → Modal como fallbacks)
  3. Agentes individuales (StyleAnalyzer, KeywordExtractor, ContentGenerator)
  4. Flujo completo del orquestador (genera post real)
  5. Supabase DB  — escribe el post generado y verifica lectura
  6. Supabase Storage — sube imagen de prueba y verifica URL pública

Uso:
    cd backend
    python test_local.py

Requiere .env con: GEMINI_API_KEY (o HF_TOKEN), SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
"""

import os, sys, json, time, uuid, traceback
from datetime import datetime
from pathlib import Path

# ── Cargar .env ───────────────────────────────────────────────────────────────
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)
    print(f"✓ .env cargado desde {env_path}\n")
else:
    print(f"⚠  No se encontró .env en {env_path}\n")

# ── Asegurarnos de que /backend y /backend/src están en el path ───────────────
BACKEND_DIR = Path(__file__).parent
for p in [str(BACKEND_DIR), str(BACKEND_DIR / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers de UI
# ─────────────────────────────────────────────────────────────────────────────
PASSED = "✅ PASS"
FAILED = "❌ FAIL"
WARN   = "⚠️  WARN"

results: list[dict] = []

def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check(name: str, ok: bool, detail: str = "", warn: bool = False):
    icon = WARN if warn else (PASSED if ok else FAILED)
    print(f"  {icon}  {name}")
    if detail:
        for line in detail.splitlines():
            print(f"         {line}")
    results.append({"name": name, "ok": ok or warn, "warn": warn, "detail": detail})

def abort(msg: str):
    print(f"\n{FAILED}  {msg}")
    print("\nAbortando — corrige este error antes de continuar.\n")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Variables de entorno
# ─────────────────────────────────────────────────────────────────────────────
section("1. Variables de entorno")

SUPABASE_URL  = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY  = (
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    or os.environ.get("SUPABASE_SERVICE_KEY")
    or os.environ.get("SUPABASE_ANON_KEY", "")
)
GEMINI_KEY    = os.environ.get("GEMINI_API_KEY", "")
HF_TOKEN      = os.environ.get("HF_TOKEN", "")
MODAL_ID      = os.environ.get("MODAL_TOKEN_ID", "")
MODAL_SECRET  = os.environ.get("MODAL_TOKEN_SECRET", "")

check("SUPABASE_URL",  bool(SUPABASE_URL),  SUPABASE_URL or "(vacío)")
check("SUPABASE_KEY",  bool(SUPABASE_KEY),  SUPABASE_KEY[:30] + "…" if SUPABASE_KEY else "(vacío)")
check("GEMINI_API_KEY", bool(GEMINI_KEY),   GEMINI_KEY[:15] + "…" if GEMINI_KEY else "(vacío)", warn=not GEMINI_KEY)
check("HF_TOKEN",      bool(HF_TOKEN),      HF_TOKEN[:15] + "…" if HF_TOKEN else "(vacío)", warn=not HF_TOKEN)
check("MODAL creds",   bool(MODAL_ID and MODAL_SECRET), "(ok)" if MODAL_ID else "(vacío)", warn=not (MODAL_ID and MODAL_SECRET))

if not (GEMINI_KEY or HF_TOKEN or (MODAL_ID and MODAL_SECRET)):
    abort("No hay ningún proveedor LLM configurado (GEMINI_API_KEY, HF_TOKEN, o MODAL creds)")
if not SUPABASE_URL or not SUPABASE_KEY:
    abort("Supabase no configurado — necesitamos SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Proveedor LLM
# ─────────────────────────────────────────────────────────────────────────────
section("2. Proveedor LLM")

try:
    from aphra_blogger.llm.factory import create_llm_provider

    # Prioridad local: Gemini → HF → auto
    # No usamos "modal" localmente porque el deployment de vLLM puede estar buildando
    local_provider = "gemini" if GEMINI_KEY else ("huggingface" if HF_TOKEN else "auto")
    provider = create_llm_provider(provider=local_provider)
    PROVIDER_NAME = local_provider
    check("Factory create_llm_provider", True, f"Provider: {provider.__class__.__name__} ({local_provider})")
    
    # Test de llamada real
    t0 = time.time()
    resp = provider.chat_completion(
        messages=[{"role": "user", "content": "Di 'hola' en una palabra."}],
        max_tokens=20,
    )
    elapsed = time.time() - t0
    check("Llamada LLM real", bool(resp.content), f"Respuesta: '{resp.content.strip()[:60]}' ({elapsed:.1f}s)")
    LLM_PROVIDER = provider
except Exception as e:
    check("Proveedor LLM", False, traceback.format_exc())
    abort("Sin proveedor LLM funcional — el resto de pruebas no tiene sentido")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Agentes individuales
# ─────────────────────────────────────────────────────────────────────────────
section("3. Agentes individuales")

PROVIDER_NAME = LLM_PROVIDER.__class__.__name__.replace("Provider", "").lower()

# 3a. StyleAnalyzer
try:
    from aphra_blogger.agents.style_analyzer import StyleAnalyzer
    sa = StyleAnalyzer(provider=PROVIDER_NAME)
    profile = sa.analyze(
        blogger_urls=["https://javipas.com"],
        sample_text="El caso es que llevo semanas pensando en esto."
    )
    has_tone = "tone" in profile
    check("StyleAnalyzer.analyze()", has_tone, f"tone={profile.get('tone','?')[:60]}")
    STYLE_PROFILE = profile
except Exception as e:
    check("StyleAnalyzer.analyze()", False, str(e))
    STYLE_PROFILE = {
        "tone": "conversacional", "voice": "primera persona",
        "expressions": ["el caso es que", "dicho y hecho"], "vocabulary": []
    }

# 3b. KeywordExtractor
try:
    from aphra_blogger.agents.keyword_extractor import KeywordExtractor
    ke = KeywordExtractor()
    # extract() real signature: (blogger_urls, sample_text=None) → dict
    kw_result = ke.extract(
        blogger_urls=["https://javipas.com"],
        sample_text="Inteligencia Artificial y el futuro del trabajo"
    )
    # Returns dict with 'keywords', 'expressions', etc.
    keywords = kw_result.get("keywords", []) if isinstance(kw_result, dict) else (kw_result or [])
    check("KeywordExtractor.extract()", bool(keywords), f"Keywords: {keywords[:5]}")
    KEYWORDS = keywords
except Exception as e:
    check("KeywordExtractor.extract()", False, str(e))
    KEYWORDS = ["inteligencia artificial", "futuro", "trabajo", "tecnología"]

# 3c. ContentGenerator — draft corto para no tardar demasiado
try:
    from aphra_blogger.agents.content_generator import ContentGenerator
    cg = ContentGenerator(provider=PROVIDER_NAME)
    t0 = time.time()
    draft = cg.generate_draft(
        topic="Inteligencia Artificial y el futuro del trabajo",
        style_profile=STYLE_PROFILE,
        keywords=KEYWORDS,
        min_words=300,
        max_words=600,
    )
    elapsed = time.time() - t0
    word_count = len(draft.split())
    check("ContentGenerator.generate_draft()", word_count > 50,
          f"{word_count} palabras ({elapsed:.1f}s)\nPrimeros 120 chars: {draft[:120].replace(chr(10), ' ')!r}")
    DRAFT_CONTENT = draft
except Exception as e:
    check("ContentGenerator.generate_draft()", False, str(e))
    DRAFT_CONTENT = "# Test post\n\nEste es un post de prueba generado localmente para diagnóstico."


# ─────────────────────────────────────────────────────────────────────────────
# 4. Orquestador completo (flujo real — puede tardar ~60s)
# ─────────────────────────────────────────────────────────────────────────────
section("4. Orquestador completo (flujo real)")
print("  ℹ️  Esto puede tardar 1-3 minutos dependiendo del LLM...\n")

ORCHESTRATOR_RESULT = None
try:
    from orchestrator.main import BloggerOrchestrator
    from orchestrator.config import OrchestratorConfig

    config = OrchestratorConfig(
        gemini_api_key=GEMINI_KEY,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        huggingface_token=HF_TOKEN,
        modal_api_key=MODAL_ID,
        provider=PROVIDER_NAME,
        enable_critique=False,   # Desactivamos critique para agilizar la prueba
        min_word_count=400,
        max_word_count=800,
        verbose=True,
    )

    orchestrator = BloggerOrchestrator(config=config, verbose=True)

    t0 = time.time()
    result = orchestrator.run(
        topic="Los retos de la IA en 2025",
        blogger_urls=["https://javipas.com"],
        output_path=None,
    )
    elapsed = time.time() - t0

    content = result.get("content", "") or result.get("final_content", "")
    html_ok = bool(result.get("html_structure"))
    kw_ok   = bool(result.get("keywords"))

    check("Orquestador: workflow_id",   bool(result.get("workflow_id")), result.get("workflow_id", "?"))
    check("Orquestador: contenido",     len(content) > 100,
          f"{len(content.split())} palabras ({elapsed:.0f}s)\n{content[:120].replace(chr(10), ' ')!r}…")
    check("Orquestador: html_structure", html_ok, str(result.get("html_structure", {}).keys())[:80])
    check("Orquestador: keywords",       kw_ok,   str(result.get("keywords", [])[:5]))
    ORCHESTRATOR_RESULT = result

except Exception as e:
    check("Orquestador completo", False, traceback.format_exc())
    # Construimos resultado mínimo sintético para poder seguir probando Supabase
    ORCHESTRATOR_RESULT = {
        "workflow_id": str(uuid.uuid4())[:8],
        "content": DRAFT_CONTENT,
        "keywords": KEYWORDS,
        "html_structure": {
            "html": f"<article><h1>Test Post</h1><p>{DRAFT_CONTENT}</p></article>",
            "metadata": {
                "title": "Test post diagnóstico",
                "slug": f"test-post-{int(time.time())}",
                "description": "Post generado por el script de diagnóstico local.",
                "word_count": len(DRAFT_CONTENT.split()),
                "reading_time": 2,
                "keywords": KEYWORDS[:5],
            }
        }
    }
    print("  ℹ️  Usando resultado sintético para continuar con pruebas de Supabase")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Supabase — tabla posts
# ─────────────────────────────────────────────────────────────────────────────
section("5. Supabase — tabla 'posts'")

POST_SLUG = None
try:
    from supabase import create_client
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    check("Supabase: cliente creado", True)

    # 5a. Leer posts actuales
    try:
        resp = sb.table("posts").select("id, slug, title, date").order("date", desc=True).limit(5).execute()
        rows = resp.data or []
        check("Supabase: leer posts", True, f"{len(rows)} posts actuales: {[r['slug'] for r in rows]}")
    except Exception as e:
        check("Supabase: leer posts", False, str(e))

    # 5b. Insertar post de prueba
    metadata = ORCHESTRATOR_RESULT.get("html_structure", {}).get("metadata", {})
    test_slug = metadata.get("slug") or f"test-local-{int(time.time())}"
    post_data = {
        "id":           ORCHESTRATOR_RESULT.get("workflow_id", str(uuid.uuid4())[:8]),
        "slug":         test_slug,
        "title":        metadata.get("title") or "Test post diagnóstico",
        "description":  metadata.get("description", "Post generado por el script de diagnóstico."),
        "content":      ORCHESTRATOR_RESULT.get("html_structure", {}).get("html", DRAFT_CONTENT),
        "author":       "Blogger Agent (local test)",
        "date":         datetime.now().strftime("%Y-%m-%d"),
        "word_count":   metadata.get("word_count") or len(DRAFT_CONTENT.split()),
        "reading_time": metadata.get("reading_time") or 2,
        "keywords":     ORCHESTRATOR_RESULT.get("keywords", KEYWORDS)[:8],
        "tags":         metadata.get("keywords", [])[:5],
        "cover_image_url": None,
    }

    try:
        ins = sb.table("posts").upsert(post_data).execute()
        inserted = ins.data
        check("Supabase: insertar post", bool(inserted),
              f"slug={test_slug}\npost_id={post_data['id']}")
        POST_SLUG = test_slug
    except Exception as e:
        check("Supabase: insertar post", False, str(e))

    # 5c. Leer el post recién insertado
    if POST_SLUG:
        try:
            read = sb.table("posts").select("*").eq("slug", POST_SLUG).single().execute()
            check("Supabase: leer post insertado", bool(read.data),
                  f"title='{read.data.get('title', '?')}'"
                  f"  keywords={read.data.get('keywords', [])[:3]}")
        except Exception as e:
            check("Supabase: leer post insertado", False, str(e))

except Exception as e:
    check("Supabase: cliente", False, traceback.format_exc())


# ─────────────────────────────────────────────────────────────────────────────
# 6. Supabase Storage — bucket 'post-images'
# ─────────────────────────────────────────────────────────────────────────────
section("6. Supabase Storage — bucket 'post-images'")

# Imagen de prueba: PNG 1×1 píxel transparente (base64 literal, no deps)
import base64, io
TINY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)
img_bytes = base64.b64decode(TINY_PNG_B64)
BUCKET = "post-images"
test_image_path = f"test/diag-{int(time.time())}.png"

try:
    sb_storage = sb.storage  # reutilizamos el cliente de arriba
    
    # 6a. Listar buckets para verificar que 'post-images' existe
    try:
        buckets = sb_storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        exists = BUCKET in bucket_names
        check(f"Supabase Storage: bucket '{BUCKET}' existe", exists,
              f"Buckets disponibles: {bucket_names}" if not exists else "")
        if not exists:
            # Intentar crear el bucket
            sb_storage.create_bucket(BUCKET, options={"public": True})
            check(f"Supabase Storage: bucket '{BUCKET}' creado", True)
    except Exception as e:
        check(f"Supabase Storage: listar buckets", False, str(e))

    # 6b. Subir imagen
    try:
        up = sb_storage.from_(BUCKET).upload(
            path=test_image_path,
            file=img_bytes,
            file_options={"content-type": "image/png", "upsert": "true"},
        )
        check("Supabase Storage: upload imagen", True, f"path={test_image_path}")
    except Exception as e:
        check("Supabase Storage: upload imagen", False, str(e))

    # 6c. Obtener URL pública
    try:
        pub = sb_storage.from_(BUCKET).get_public_url(test_image_path)
        check("Supabase Storage: URL pública", bool(pub), pub)

        # 6d. Verificar que la URL responde 200
        import urllib.request
        req = urllib.request.Request(pub, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                status = r.status
            check("Supabase Storage: URL accesible (HEAD)", status == 200, f"HTTP {status}")
        except Exception as e:
            check("Supabase Storage: URL accesible", False, str(e), warn=True)

    except Exception as e:
        check("Supabase Storage: URL pública", False, str(e))

    # 6e. Actualizar el post de prueba con la imagen si fue insertado
    if POST_SLUG:
        try:
            img_url = sb_storage.from_(BUCKET).get_public_url(test_image_path)
            sb.table("posts").update({"cover_image_url": img_url}).eq("slug", POST_SLUG).execute()
            check("Supabase: actualizar post con cover_image_url", True, img_url[:80])
        except Exception as e:
            check("Supabase: actualizar post con cover_image_url", False, str(e))

except NameError:
    check("Supabase Storage", False, "Cliente Supabase no disponible (falló en §5)")
except Exception as e:
    check("Supabase Storage", False, traceback.format_exc())


# ─────────────────────────────────────────────────────────────────────────────
# Resumen final
# ─────────────────────────────────────────────────────────────────────────────
section("RESUMEN")

passed = [r for r in results if r["ok"] and not r["warn"]]
warned = [r for r in results if r["warn"]]
failed = [r for r in results if not r["ok"]]

print(f"  ✅  {len(passed)} passed")
if warned:
    print(f"  ⚠️   {len(warned)} warnings")
if failed:
    print(f"  ❌  {len(failed)} failed")

if failed:
    print("\n  FALLOS DETECTADOS:")
    for r in failed:
        print(f"    • {r['name']}")
        if r["detail"]:
            for line in r["detail"].splitlines()[:3]:
                print(f"        {line}")
else:
    print("\n  🎉  ¡Todo el sistema funciona correctamente!")

if POST_SLUG:
    print(f"\n  📝  Post de prueba guardado en Supabase:")
    print(f"      slug: {POST_SLUG}")
    print(f"      URL:  {SUPABASE_URL}/rest/v1/posts?slug=eq.{POST_SLUG}")

print()

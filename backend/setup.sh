#!/bin/bash
# Setup script para el backend usando uv
# 
# Este script automatiza el setup del entorno de desarrollo usando uv,
# el gestor de paquetes Python ultrarrápido.
#
# Uso:
#   ./setup.sh

set -e  # Exit on error

echo "================================================"
echo "🚀 Setup del Backend - Blogger Agent TFG"
echo "================================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv no está instalado"
    echo ""
    echo "Instalando uv..."
    
    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "❌ Sistema operativo no soportado para instalación automática"
        echo "Por favor, instala uv manualmente:"
        echo "  https://github.com/astral-sh/uv"
        exit 1
    fi
else
    echo "✅ uv ya está instalado ($(uv --version))"
fi

echo ""
echo "📦 Creando entorno virtual..."
uv venv

echo ""
echo "📥 Instalando dependencias..."
uv pip install -r requirements.txt

echo ""
echo "================================================"
echo "✅ Setup completado!"
echo "================================================"
echo ""
echo "Para activar el entorno virtual:"
echo ""
echo "  source .venv/bin/activate"
echo ""
echo "Para ejecutar el orquestador:"
echo ""
echo "  python -m src.orchestrator.runner \\"
echo "    --topic \"Tu Topic\" \\"
echo "    --blog-url \"https://blog.ejemplo.com\" \\"
echo "    --output \"resultado.json\""
echo ""
echo "Para ejecutar tests:"
echo ""
echo "  pytest tests/ -v"
echo ""

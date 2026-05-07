# Setup script para el backend usando uv (Windows PowerShell)
# 
# Este script automatiza el setup del entorno de desarrollo usando uv
#
# Uso: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup del Backend - Blogger Agent TFG" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if uv is installed
try {
    $uvVersion = uv --version 2>$null
    Write-Host "[OK] uv ya esta instalado ($uvVersion)" -ForegroundColor Green
} catch {
    Write-Host "[!] uv no esta instalado" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Instalando uv..." -ForegroundColor Yellow
    
    try {
        irm https://astral.sh/uv/install.ps1 | iex
        Write-Host "[OK] uv instalado correctamente" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Error instalando uv" -ForegroundColor Red
        Write-Host "Por favor, instala uv manualmente:" -ForegroundColor Red
        Write-Host "  https://github.com/astral-sh/uv" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
uv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error creando entorno virtual" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Cyan
uv pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error instalando dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "[OK] Setup completado!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para activar el entorno virtual:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Para ejecutar el orquestador:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  python -m src.orchestrator.runner ``" -ForegroundColor White
Write-Host "    --topic 'Tu Topic' ``" -ForegroundColor White
Write-Host "    --blog-url 'https://blog.ejemplo.com' ``" -ForegroundColor White
Write-Host "    --output 'resultado.json'" -ForegroundColor White
Write-Host ""
Write-Host "Para ejecutar tests:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  pytest tests/ -v" -ForegroundColor White
Write-Host ""

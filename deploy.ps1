# Script para desplegar la carpeta docs/ a la rama gh-pages de forma limpia
# Uso: powershell -ExecutionPolicy Bypass -File deploy.ps1

Write-Host "🚀 Iniciando despliegue en GitHub Pages..." -ForegroundColor Cyan

# 1. Asegurarse de que estamos en la raíz del proyecto
$RootPath = (Get-Item -Path $PSScriptRoot).Parent.FullName
if ($PSScriptRoot -like "*backend*") {
    $RootPath = (Get-Item -Path $PSScriptRoot).Parent.FullName
} else {
    $RootPath = $PWD.Path
}
Set-Location $RootPath

# 2. Verificar que la carpeta docs existe
if (-not (Test-Path "docs")) {
    Write-Error "❌ Error: La carpeta docs/ no existe."
    exit 1
}

# 3. Empujar la carpeta docs a la rama gh-pages usando git subtree
# Esto evita tener que usar filter-branch que es lento y destructivo
Write-Host "📦 Extrayendo carpeta docs/ y enviando a la rama gh-pages..." -ForegroundColor Yellow

# Eliminar rama local gh-pages si existe para evitar conflictos
git branch -D gh-pages 2>$null

# Comando mágico: crea una rama a partir de una subcarpeta y la empuja
try {
    # Usamos subtree push para enviar la carpeta docs/ directamente a origin gh-pages
    git subtree push --prefix docs origin gh-pages
    Write-Host "✅ ¡Despliegue completado con éxito!" -ForegroundColor Green
    Write-Host "🌐 URL: https://AlejandroRS21.github.io/blogger-agent-tfg/" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error durante el despliegue. Asegúrate de que no haya cambios sin commitear en la carpeta docs/." -ForegroundColor Red
    exit 1
}

# Script para desplegar la carpeta docs/ a la rama gh-pages de forma limpia
# Uso: powershell -ExecutionPolicy Bypass -File deploy.ps1

Write-Host "Iniciando despliegue en GitHub Pages..." -ForegroundColor Cyan

# 1. Asegurarse de que estamos en la raíz del proyecto
Set-Location "d:\PROYECTOS\Big Data IA\Modelos de IA\blogger-agent-tfg"

# 2. Verificar que la carpeta docs existe
if (-not (Test-Path "docs")) {
    Write-Host "Error: La carpeta docs/ no existe." -ForegroundColor Red
    exit 1
}

# 3. Empujar la carpeta docs a la rama gh-pages usando git subtree
Write-Host "Extraigo carpeta docs/ y enviando a la rama gh-pages..." -ForegroundColor Yellow

# Eliminar rama local gh-pages si existe para evitar conflictos
git branch -D gh-pages 2>$null

# Usamos subtree push para enviar la carpeta docs/ directamente a origin gh-pages
try {
    git subtree push --prefix docs origin gh-pages
    Write-Host "Despliegue completado con exito!" -ForegroundColor Green
    Write-Host "URL: https://AlejandroRS21.github.io/blogger-agent-tfg/" -ForegroundColor Cyan
}
catch {
    Write-Host "Error durante el despliegue." -ForegroundColor Red
    exit 1
}

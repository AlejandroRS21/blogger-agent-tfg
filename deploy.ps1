# Script para desplegar la carpeta docs/ a la rama gh-pages
# Uso: powershell -ExecutionPolicy Bypass -File deploy.ps1
#      ./deploy.sh  (Linux/macOS)

Write-Host "Iniciando despliegue en GitHub Pages..." -ForegroundColor Cyan

# 1. Detectar la raíz del proyecto (directorio donde está este script)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# 2. Verificar que la carpeta docs existe
if (-not (Test-Path "docs")) {
    Write-Host "Error: La carpeta docs/ no existe." -ForegroundColor Red
    exit 1
}

# 3. Empujar la carpeta docs a la rama gh-pages usando git subtree
Write-Host "Enviando carpeta docs/ a la rama gh-pages..." -ForegroundColor Yellow

# Eliminar rama local gh-pages si existe para evitar conflictos
git branch -D gh-pages 2>$null

# Usamos subtree push para enviar docs/ directamente a origin gh-pages
try {
    git subtree push --prefix docs origin gh-pages
    Write-Host "Despliegue completado con exito!" -ForegroundColor Green
    
    # Detectar URL del remote
    $RemoteUrl = git remote get-url origin 2>$null
    if ($RemoteUrl -match "github\.com[:/](.+?)/(.+?)(\.git)?$") {
        $User = $Matches[1]
        $Repo = $Matches[2] -replace '\.git$', ''
        Write-Host "URL: https://${User}.github.io/${Repo}/" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "Error durante el despliegue." -ForegroundColor Red
    exit 1
}

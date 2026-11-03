# ==============================================================================
# RADAR TECH RECIFE - SCRIPT DE PROVISIONAMENTO E SETUP DE AMBIENTE
# Arquitetura Soberana: UTF-8 com BOM e CRLF (PowerShell 5.1 / 7+)
# ==============================================================================

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   RADAR TECH RECIFE - INICIALIZANDO AMBIENTE       " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# 1. Verifica se Python esta instalado
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERRO] Python nao foi encontrado no PATH do sistema." -ForegroundColor Red
    Write-Host "Instale o Python 3.10+ e tente novamente." -ForegroundColor Yellow
    Exit 1
}

# 2. Criacao do Virtual Environment (.venv) caso nao exista
$venvPath = Join-Path -Path $PSScriptRoot -ChildPath "..\.venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[INFO] Criando ambiente virtual em .venv..." -ForegroundColor Green
    python -m venv $venvPath
} else {
    Write-Host "[INFO] Ambiente virtual .venv ja existe." -ForegroundColor Gray
}

# 3. Caminho do executavel pip dentro da venv
$pipExe = Join-Path -Path $venvPath -ChildPath "Scripts\pip.exe"
$pythonExe = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"

Write-Host "[INFO] Atualizando pip..." -ForegroundColor Green
& $pipExe install --upgrade pip --quiet

# 4. Instalacao das dependencias do requirements.txt
$reqPath = Join-Path -Path $PSScriptRoot -ChildPath "..\requirements.txt"
if (Test-Path $reqPath) {
    Write-Host "[INFO] Instalando dependencias de requirements.txt..." -ForegroundColor Green
    & $pipExe install -r $reqPath
}

# 5. Criacao da pasta de dados SQLite
$dataDir = Join-Path -Path $PSScriptRoot -ChildPath "..\data"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "[INFO] Pasta data/ provisionada com sucesso." -ForegroundColor Green
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   AMBIENTE PRONTO COM SUCESSO!                     " -ForegroundColor Green
Write-Host "Para rodar o radar: .\scripts\run_radar.ps1          " -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Cyan

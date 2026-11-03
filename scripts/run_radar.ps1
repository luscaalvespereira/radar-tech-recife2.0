# ==============================================================================
# RADAR TECH RECIFE - EXECUCAO CONTINUA DO RADAR
# Arquitetura Soberana: UTF-8 com BOM e CRLF (PowerShell 5.1 / 7+)
# ==============================================================================

$rootPath = Resolve-Path (Join-Path -Path $PSScriptRoot -ChildPath "..")
Set-Location $rootPath

$pythonExe = Join-Path -Path $rootPath -ChildPath ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   INICIANDO RADAR TECH RECIFE                      " -ForegroundColor Cyan
Write-Host "   Monitorando Porto Digital, CESAR, O NERD e mais  " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

& $pythonExe radar.py

# ==============================================================================
# RADAR TECH RECIFE - TESTE DE COMUNICACAO COM O TELEGRAM
# Arquitetura Soberana: UTF-8 com BOM e CRLF (PowerShell 5.1 / 7+)
# ==============================================================================

$rootPath = Resolve-Path (Join-Path -Path $PSScriptRoot -ChildPath "..")
Set-Location $rootPath

$pythonExe = Join-Path -Path $rootPath -ChildPath ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Write-Host "[INFO] Testando envio de alerta para o Telegram..." -ForegroundColor Cyan
& $pythonExe radar.py --test-telegram

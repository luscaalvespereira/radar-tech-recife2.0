# ==============================================================================
# RADAR TECH RECIFE - INSPECAO DO BANCO DE DADOS E HISTORICO
# Arquitetura Soberana: UTF-8 com BOM e CRLF (PowerShell 5.1 / 7+)
# ==============================================================================

$rootPath = Resolve-Path (Join-Path -Path $PSScriptRoot -ChildPath "..")
Set-Location $rootPath

$pythonExe = Join-Path -Path $rootPath -ChildPath ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Write-Host "=== Estatisticas do Banco SQLite ===" -ForegroundColor Cyan
& $pythonExe query_db.py --stats

Write-Host "=== Top Oportunidades por Score ===" -ForegroundColor Green
& $pythonExe query_db.py -n 20

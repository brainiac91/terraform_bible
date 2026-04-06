<#
.SYNOPSIS
Starts the Terraform Bible Platform via Docker Compose.

.DESCRIPTION
This script builds and starts the local learning environment using docker-compose.
It has been optimized to detect Docker both natively on Windows and within WSL (Ubuntu).
The platform will be available at http://localhost:8000.
#>

Write-Host "Starting Terraform Bible Platform..." -ForegroundColor Cyan

$hasWinDockerCompose = $false
try {
    if (Get-Command "docker" -ErrorAction SilentlyContinue) {
        $null = docker compose version 2>$null
        if ($LASTEXITCODE -eq 0) { $hasWinDockerCompose = $true }
    }
} catch { }

$hasWinDockerComposeV1 = [bool](Get-Command "docker-compose" -ErrorAction SilentlyContinue)

$hasWslDockerCompose = $false
try {
    if (Get-Command "wsl" -ErrorAction SilentlyContinue) {
        $null = wsl docker compose version 2>$null
        if ($LASTEXITCODE -eq 0) { $hasWslDockerCompose = $true }
    }
} catch { }

$hasWslDockerComposeV1 = $false
try {
    if (Get-Command "wsl" -ErrorAction SilentlyContinue) {
        $null = wsl docker-compose --version 2>$null
        if ($LASTEXITCODE -eq 0) { $hasWslDockerComposeV1 = $true }
    }
} catch { }

if ($hasWinDockerCompose) {
    Write-Host "Detected native Docker Compose v2." -ForegroundColor Green
    docker compose up --build -d
} elseif ($hasWinDockerComposeV1) {
    Write-Host "Detected native Docker-Compose v1." -ForegroundColor Green
    docker-compose up --build -d
} elseif ($hasWslDockerCompose) {
    Write-Host "Detected Docker Compose inside WSL. Delegating execution to WSL..." -ForegroundColor Yellow
    wsl docker compose up --build -d
} elseif ($hasWslDockerComposeV1) {
    Write-Host "Detected Docker-Compose inside WSL. Delegating execution to WSL..." -ForegroundColor Yellow
    wsl docker-compose up --build -d
} else {
    Write-Host "`n[ERROR] Neither docker-compose nor docker compose found in Windows PATH or WSL. Please install Docker." -ForegroundColor Red
    exit 1
}

Write-Host "`n[SUCCESS] Platform execution triggered successfully!" -ForegroundColor Green
Write-Host "It should be running at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Note: Stop it using the applicable down command (e.g. 'wsl docker compose down')" -ForegroundColor Yellow

# Start development environment using Docker Compose
# Usage: .\scripts\start-dev.ps1

param(
    [switch]$foreground = $false
)

Write-Host "[*] Starting AI Interview & Resume Agent development environment..." -ForegroundColor Green

# Check Docker
if (-Not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Docker not found. Please install Docker Desktop: https://www.docker.com/get-started" -ForegroundColor Red
    exit 1
}

# Determine docker compose command
$composeCmd = "docker"
$composeArgs = @("compose")

# Test if 'docker compose' works, fall back to docker-compose if not
$testCompose = & docker compose version 2>&1
if ($LASTEXITCODE -ne 0) {
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        $composeCmd = "docker-compose"
        $composeArgs = @()
    } else {
        Write-Host "[!] Docker Compose not found. Update Docker Desktop or install docker-compose." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[+] Using: $composeCmd $($composeArgs -join ' ')" -ForegroundColor Cyan

# Create .env if missing
if (-Not (Test-Path .env)) {
    Write-Host "[*] Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "[!] Review .env and add real secrets (OPENAI_API_KEY, STRIPE_API_KEY, etc.)" -ForegroundColor Yellow
}

# Build and start
Write-Host "[*] Starting services..." -ForegroundColor Cyan
if ($foreground) {
    & $composeCmd @composeArgs up --build
} else {
    & $composeCmd @composeArgs up --build -d
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Failed to start services" -ForegroundColor Red
    exit 1
}

if (-Not $foreground) {
    Write-Host "[+] Services started in background" -ForegroundColor Green
    Start-Sleep -Seconds 5
    
    Write-Host "`n[*] Container status:" -ForegroundColor Cyan
    & $composeCmd @composeArgs ps
    
    Write-Host "`n[*] Recent backend logs:" -ForegroundColor Cyan
    & $composeCmd @composeArgs logs backend --tail 30
    
    Write-Host "`n[*] Creating admin user..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    & $composeCmd @composeArgs exec -T backend python scripts/create_admin.py --email admin@example.com --password secret
    
    Write-Host "`n[OK] Services running!" -ForegroundColor Green
    Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  MinIO:    http://localhost:9000 (user: miniouser, pass: miniosecret)" -ForegroundColor Cyan
    Write-Host "`n[*] Commands:" -ForegroundColor Yellow
    Write-Host "  View logs:     $composeCmd $($composeArgs -join ' ') logs -f backend" -ForegroundColor Yellow
    Write-Host "  Stop services: $composeCmd $($composeArgs -join ' ') down" -ForegroundColor Yellow
}
else {
    Write-Host "`n[OK] Services running in foreground (Ctrl+C to stop)" -ForegroundColor Green
}

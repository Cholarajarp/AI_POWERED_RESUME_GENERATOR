# Start development environment using Docker Compose
# Usage: .\scripts\start-dev.ps1

param(
    [switch]$foreground = $false,
    [switch]$rebuild = $false
)

Write-Host "🚀 Starting AI Interview & Resume Agent development environment..." -ForegroundColor Green

# Check Docker
$dockerCmd = $null
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $dockerCmd = "docker"
}
else {
    Write-Host "❌ Docker not found. Please install Docker Desktop: https://www.docker.com/get-started" -ForegroundColor Red
    exit 1
}

# Determine docker compose command
$composeCmd = @()
if (& docker compose version *>$null 2>&1) {
    $composeCmd = @("docker", "compose")
} elseif (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    $composeCmd = @("docker-compose")
} else {
    Write-Host "❌ Docker Compose not found. Update Docker Desktop or install docker-compose." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Using: $($composeCmd -join ' ')" -ForegroundColor Cyan

# Create .env if missing
if (-Not (Test-Path .env)) {
    Write-Host "📝 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Review .env and add real secrets (OPENAI_API_KEY, STRIPE_API_KEY, etc.)" -ForegroundColor Yellow
}

# Build and start
$upArgs = @("up", "--build")
if (-Not $foreground) {
    $upArgs += "-d"
}

Write-Host "🐳 Starting services..." -ForegroundColor Cyan
& $composeCmd $upArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    exit 1
}

if (-Not $foreground) {
    Write-Host "✓ Services started in background" -ForegroundColor Green
    Start-Sleep -Seconds 3
    
    Write-Host "`n📊 Container status:" -ForegroundColor Cyan
    & $composeCmd ps
    
    Write-Host "`n📋 Recent backend logs:" -ForegroundColor Cyan
    & $composeCmd logs backend --tail 30
    
    Write-Host "`n🔧 Creating admin user..." -ForegroundColor Cyan
    Start-Sleep -Seconds 2
    & $composeCmd exec -T backend python scripts/create_admin.py --email admin@example.com --password secret
    
    Write-Host "`n✅ Services running!" -ForegroundColor Green
    Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  MinIO:    http://localhost:9000 (user: miniouser, pass: miniosecret)" -ForegroundColor Cyan
    Write-Host "`n💡 View logs: $($composeCmd -join ' ') logs -f backend" -ForegroundColor Yellow
    Write-Host "💡 Stop services: $($composeCmd -join ' ') down" -ForegroundColor Yellow
} else {
    Write-Host "`n✅ Services running in foreground (press Ctrl+C to stop)" -ForegroundColor Green
}

# ==============================================================================
# PowerShell Development Scripts for Windows
# ==============================================================================
# Alternative to Makefile for Windows users
# Usage: .\dev.ps1 <command>
# ==============================================================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Colors
$Cyan = "Cyan"
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"

function Show-Help {
    Write-Host "`n=== AI Business Assistant - PowerShell Commands ===" -ForegroundColor $Cyan
    Write-Host ""
    Write-Host "DEVELOPMENT:" -ForegroundColor $Green
    Write-Host "  .\dev.ps1 dev              Start development environment"
    Write-Host "  .\dev.ps1 dev-build        Build and start development"
    Write-Host "  .\dev.ps1 stop             Stop all containers"
    Write-Host "  .\dev.ps1 restart          Restart containers"
    Write-Host ""
    Write-Host "LOGS:" -ForegroundColor $Green
    Write-Host "  .\dev.ps1 logs             Show all logs"
    Write-Host "  .\dev.ps1 logs-api         Show API logs"
    Write-Host "  .\dev.ps1 logs-bot         Show bot logs"
    Write-Host "  .\dev.ps1 logs-db          Show database logs"
    Write-Host ""
    Write-Host "DATABASE:" -ForegroundColor $Green
    Write-Host "  .\dev.ps1 migrate          Run database migrations"
    Write-Host "  .\dev.ps1 backup           Create database backup"
    Write-Host "  .\dev.ps1 db-shell         Open PostgreSQL shell"
    Write-Host ""
    Write-Host "TESTING:" -ForegroundColor $Green
    Write-Host "  .\dev.ps1 test             Run all tests"
    Write-Host "  .\dev.ps1 test-unit        Run unit tests"
    Write-Host "  .\dev.ps1 lint             Run linters"
    Write-Host ""
    Write-Host "UTILITIES:" -ForegroundColor $Green
    Write-Host "  .\dev.ps1 ps               Show running containers"
    Write-Host "  .\dev.ps1 stats            Show container resource usage"
    Write-Host "  .\dev.ps1 shell-api        Open shell in API container"
    Write-Host "  .\dev.ps1 env-check        Validate .env configuration"
    Write-Host ""
}

# Development commands
function Start-Dev {
    Write-Host "Starting development environment..." -ForegroundColor $Cyan
    docker-compose up -d
    Write-Host "✓ Development environment started" -ForegroundColor $Green
    Write-Host "  API: http://localhost:8000" -ForegroundColor $Yellow
    Write-Host "  Docs: http://localhost:8000/api/docs" -ForegroundColor $Yellow
}

function Start-DevBuild {
    Write-Host "Building and starting development environment..." -ForegroundColor $Cyan
    docker-compose up -d --build
    Write-Host "✓ Development environment started" -ForegroundColor $Green
}

function Stop-Dev {
    Write-Host "Stopping containers..." -ForegroundColor $Cyan
    docker-compose down
    Write-Host "✓ Containers stopped" -ForegroundColor $Green
}

function Restart-Dev {
    Write-Host "Restarting containers..." -ForegroundColor $Cyan
    Stop-Dev
    Start-Dev
}

# Logs
function Show-Logs {
    docker-compose logs -f
}

function Show-ApiLogs {
    docker-compose logs -f api
}

function Show-BotLogs {
    docker-compose logs -f bot
}

function Show-DbLogs {
    docker-compose logs -f db
}

# Database
function Run-Migrate {
    Write-Host "Running database migrations..." -ForegroundColor $Cyan
    docker-compose exec api alembic upgrade head
    Write-Host "✓ Migrations complete" -ForegroundColor $Green
}

function Create-Backup {
    Write-Host "Creating database backup..." -ForegroundColor $Cyan
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    docker-compose exec db sh -c "pg_dump -U `$DB_USER `$DB_NAME | gzip > /backups/backup_$timestamp.sql.gz"
    Write-Host "✓ Backup created: backups/backup_$timestamp.sql.gz" -ForegroundColor $Green
}

function Open-DbShell {
    docker-compose exec db psql -U $env:DB_USER -d $env:DB_NAME
}

# Testing
function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor $Cyan
    pytest tests/ -v --cov=. --cov-report=html --cov-report=term
    Write-Host "✓ Tests complete" -ForegroundColor $Green
}

function Run-UnitTests {
    Write-Host "Running unit tests..." -ForegroundColor $Cyan
    pytest tests/unit/ -v
    Write-Host "✓ Unit tests complete" -ForegroundColor $Green
}

function Run-Lint {
    Write-Host "Running linters..." -ForegroundColor $Cyan
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    Write-Host "✓ Linting complete" -ForegroundColor $Green
}

# Utilities
function Show-Ps {
    docker-compose ps
}

function Show-Stats {
    docker stats
}

function Open-ApiShell {
    docker-compose exec api /bin/bash
}

function Check-Env {
    Write-Host "Checking environment configuration..." -ForegroundColor $Cyan
    python -m config.settings
    Write-Host "✓ Environment check complete" -ForegroundColor $Green
}

# Command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }

    # Development
    "dev" { Start-Dev }
    "dev-build" { Start-DevBuild }
    "stop" { Stop-Dev }
    "restart" { Restart-Dev }

    # Logs
    "logs" { Show-Logs }
    "logs-api" { Show-ApiLogs }
    "logs-bot" { Show-BotLogs }
    "logs-db" { Show-DbLogs }

    # Database
    "migrate" { Run-Migrate }
    "backup" { Create-Backup }
    "db-shell" { Open-DbShell }

    # Testing
    "test" { Run-Tests }
    "test-unit" { Run-UnitTests }
    "lint" { Run-Lint }

    # Utilities
    "ps" { Show-Ps }
    "stats" { Show-Stats }
    "shell-api" { Open-ApiShell }
    "env-check" { Check-Env }

    default {
        Write-Host "Unknown command: $Command" -ForegroundColor $Red
        Write-Host "Run '.\dev.ps1 help' to see available commands" -ForegroundColor $Yellow
    }
}

<#
.SYNOPSIS
    Setup script for dataset-downloader on Windows
.DESCRIPTION
    Downloads uv, creates a virtual environment, and installs dependencies
#>

$ErrorActionPreference = "Stop"

Write-Host "=== Dataset Downloader Setup ===" -ForegroundColor Cyan

# Check if uv is already installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvInstalled) {
    Write-Host "Installing uv..." -ForegroundColor Yellow

    # Download and run the official uv installer
    irm https://astral.sh/uv/install.ps1 | iex

    # Refresh PATH for current session
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

    # Verify installation
    $uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uvInstalled) {
        Write-Host "uv installation failed. Please restart your terminal and try again." -ForegroundColor Red
        exit 1
    }
    Write-Host "uv installed successfully!" -ForegroundColor Green
} else {
    Write-Host "uv is already installed." -ForegroundColor Green
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
uv venv .venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to create virtual environment." -ForegroundColor Red
    exit 1
}
Write-Host "Virtual environment created." -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv pip install -r dependencies.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "To activate the virtual environment, run:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""

# Market Risk Analysis Dashboard Launcher
# PowerShell Script

Write-Host "🚀 Starting Market Risk Analysis Dashboard..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Yellow
try {
    python -c "import streamlit, pandas, yfinance" 2>$null
    Write-Host "✓ All required packages are installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Some packages are missing. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install packages. Please run 'pip install -r requirements.txt' manually." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Launching dashboard..." -ForegroundColor Green
Write-Host "The dashboard will open in your default web browser." -ForegroundColor Cyan
Write-Host "If it doesn't open automatically, go to: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the dashboard." -ForegroundColor Yellow
Write-Host ""

# Launch the dashboard
streamlit run dashboard.py 
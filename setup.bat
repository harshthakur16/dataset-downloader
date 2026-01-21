@echo off
:: Setup script for dataset-downloader on Windows
:: This batch file runs the PowerShell setup script

echo === Dataset Downloader Setup ===

:: Check PowerShell execution policy and run the script
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo Setup failed.
    pause
    exit /b 1
)

pause

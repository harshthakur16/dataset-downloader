@echo off
setlocal enabledelayedexpansion

REM Create venv if missing
if not exist .venv (
  py -3 -m venv .venv 2>nul || python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Ensure .env exists or prompt for key
if not exist .env (
  if exist .env.example copy .env.example .env >nul
  set /p SEEKHO_API_KEY=Enter your SEEKHO API key: 
  powershell -Command "(Get-Content .env) -replace 'SEEKHO_API_KEY=.*', 'SEEKHO_API_KEY=%SEEKHO_API_KEY%' | Set-Content .env"
)

REM Run the tool
python -m seekho_downloader --out dataset.csv
echo.
echo Done. You can find dataset.csv in this folder.
pause

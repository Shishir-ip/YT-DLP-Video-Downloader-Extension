@echo off
title YT-DLP Bridge Server
color 0B
cls

echo ================================================
echo      YT-DLP Bridge Server
echo ================================================
echo.

cd /d "%~dp0backend"

echo [Check] Ensuring Flask is installed...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo [Install] Flask not found. Installing flask + flask-cors...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Flask. Run: python -m pip install flask flask-cors
        pause
        exit /b 1
    )
)
echo [OK] Flask ready.
echo.

echo [Launch] Starting server on http://127.0.0.1:8765
echo [Info] Keep this window open while using the extension.
echo.

python yt-dlp-bridge.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server crashed with code %errorlevel%.
    pause
)

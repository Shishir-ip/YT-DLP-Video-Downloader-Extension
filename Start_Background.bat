@echo off
title YT-DLP Background Start
color 0B
cls

echo ================================================
echo   Starting YT-DLP Server in Background
echo ================================================
echo.

cd /d "%~dp0backend"

echo [Step 1] Checking Flask...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo [Install] Flask missing. Installing...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Flask.
        pause
        exit /b 1
    )
)
echo [OK] Flask ready.
echo.

echo [Step 2] Finding pythonw.exe...
set "PY_EXE=pythonw.exe"
pythonw --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Found pythonw.exe (no window)
    goto :start_it
)

for /f "tokens=*" %%a in ('where python.exe 2^>nul') do (
    if exist "%%~dpapythonw.exe" (
        set "PY_EXE=%%~dpapythonw.exe"
        echo [OK] Found pythonw.exe next to python.exe
        goto :start_it
    )
)

set "PY_EXE=python.exe"
echo [Note] Using python.exe with hidden window.

:start_it
echo.
echo [Step 3] Starting server...

taskkill /F /IM python.exe /FI "WINDOWTITLE eq YT-DLP Bridge Server" >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 1 /nobreak >nul

if "%PY_EXE%"=="python.exe" (
    start /min "" "%PY_EXE%" yt-dlp-bridge.py
) else (
    start "" "%PY_EXE%" yt-dlp-bridge.py
)

echo [OK] Server process launched.
echo.

echo [Step 4] Verifying server is up...
timeout /t 2 /nobreak >nul
python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/health').read()" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Server is RUNNING on http://127.0.0.1:8765
    echo.
    echo ================================================
    echo   SUCCESS! You can now use the extension.
    echo ================================================
) else (
    echo [WARN] Server still starting. Wait 3 seconds and try again.
    echo        Or run Start_Server.bat for visible window.
)

echo.
pause

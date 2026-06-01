@echo off
title YT-DLP Server Check
color 0B
cls

echo ================================================
echo   YT-DLP Server Check
echo ================================================
echo.

echo [1] Testing server on http://127.0.0.1:8765 ...
python -c "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8765/health'); print(r.read().decode())" 2>nul
if %errorlevel% equ 0 (
    echo.
    echo [OK] Server is RUNNING and responding!
    echo.
    echo ================================================
    echo   The extension should work now.
    echo ================================================
    goto :end
)

echo [FAIL] Server is NOT responding.
echo.

echo [2] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%a in ('python --version') do echo [OK] %%a
) else (
    echo [FAIL] Python not found in PATH.
    echo        Reinstall Python and check "Add to PATH".
    goto :end
)

echo.
echo [3] Checking Flask...
python -c "import flask" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Flask is installed.
) else (
    echo [FAIL] Flask is NOT installed.
    echo        Run: python -m pip install flask flask-cors
    echo.
    goto :end
)

echo.
echo [4] Checking yt-dlp...
yt-dlp --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%a in ('yt-dlp --version') do echo [OK] yt-dlp version %%a
) else (
    echo [WARN] yt-dlp not in PATH. Make sure yt-dlp.exe is in Downloads.
)

echo.
echo ================================================
echo   Server is NOT running. To fix:
echo.
echo   1. Run:  Start_Server.bat  (visible window, easiest)
echo   2. Or:   Start_Background.bat  (no window)
echo ================================================

:end
echo.
pause

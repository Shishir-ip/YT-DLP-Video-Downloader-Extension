@echo off
title Remove YT-DLP Server from Startup
color 0C
cls

set "LNK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\YT-DLP-Server.lnk"
set "VBS=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\YT-DLP-Server.vbs"

if exist "%LNK%" (
    del /F "%LNK%"
    echo [OK] Removed startup shortcut.
)
if exist "%VBS%" (
    del /F "%VBS%"
    echo [OK] Removed old startup VBS.
)

echo.
echo Stopping any running server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq YT-DLP Bridge Server" >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
echo [OK] Stopped.
echo.
pause

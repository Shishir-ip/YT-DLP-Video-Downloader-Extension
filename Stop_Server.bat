@echo off
title Stop YT-DLP Server
color 0C
cls

echo Stopping YT-DLP Server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq YT-DLP Bridge Server" >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
echo [OK] Server stopped.
echo.
pause

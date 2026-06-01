@echo off
title Add YT-DLP Server to Startup
color 0B
cls

echo ================================================
echo   Add YT-DLP Server to Windows Startup
echo ================================================
echo.

set "SOURCE=%~dp0Start_Background.bat"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

if not exist "%SOURCE%" (
    echo [ERROR] Start_Background.bat not found.
    pause
    exit /b 1
)

echo [Step 1] Creating startup shortcut...
set "VBS_TEMP=%TEMP%\make_shortcut.vbs"
(
echo Set WshShell = CreateObject("WScript.Shell")
echo Set oLink = WshShell.CreateShortcut("%STARTUP_DIR%\YT-DLP-Server.lnk")
echo oLink.TargetPath = "%SOURCE%"
echo oLink.WorkingDirectory = "%~dp0"
echo oLink.IconLocation = "shell32.dll,21"
echo oLink.Save
) > "%VBS_TEMP%"
cscript //nologo "%VBS_TEMP%"
del "%VBS_TEMP%"

echo [OK] Added shortcut to startup.
echo.

echo [Step 2] Starting server now...
call "%SOURCE%"

echo.
echo ================================================
echo   DONE! Server will auto-start on every login.
echo   To remove: Run Remove_from_Startup.bat
echo ================================================
echo.
pause

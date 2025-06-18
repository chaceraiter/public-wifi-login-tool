@echo off
REM Public WiFi Login Tool - Installation Script for Windows

echo Public WiFi Login Tool - Installation
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version% detected

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✓ pip detected

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Check if Chrome is installed (for GUI version)
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if errorlevel 1 (
    reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
    if errorlevel 1 (
        echo ⚠ Chrome not detected in registry. GUI version may not work properly.
        echo   You can still use the CLI version.
    ) else (
        echo ✓ Chrome detected (for GUI version)
    )
) else (
    echo ✓ Chrome detected (for GUI version)
)

echo.
echo Installation complete!
echo.
echo Usage:
echo   GUI version: python wifi_login_tool.py
echo   CLI version: python wifi_login_cli.py
echo.
echo For more information, see README.md
echo.
echo ⚠️  WARNING: Only use this tool on networks you trust!
pause 
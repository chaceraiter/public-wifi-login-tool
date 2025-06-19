@echo off
REM Public WiFi Login Tool - Installation Script for Windows

echo Public WiFi Login Tool - Installation
echo =====================================
echo.

REM Check if Docker is installed and running
echo Checking Docker availability...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH.
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo After installation, restart your computer and run this script again.
    pause
    exit /b 1
)

echo ✓ Docker detected

REM Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker daemon is not running.
    echo.
    echo Please start Docker Desktop and wait for it to fully load, then run this script again.
    pause
    exit /b 1
)

echo ✓ Docker daemon is running

REM Build the Docker image
echo.
echo Building Docker image...
docker build -t wifi-login-tool .

if errorlevel 1 (
    echo ❌ Failed to build Docker image
    pause
    exit /b 1
)

echo ✓ Docker image built successfully

REM Create shortcuts
echo.
echo Creating shortcuts...

REM Get current directory
set CURRENT_DIR=%CD%

REM Create desktop shortcut for CLI version
if exist "%USERPROFILE%\Desktop" (
    echo @echo off > "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo echo Starting WiFi Login Tool... >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo docker-compose up wifi-login-cli >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo pause >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo ✓ Desktop CLI shortcut created
) else (
    echo ⚠ Desktop directory not found, skipping desktop shortcut
)

REM Create desktop shortcut for headless version
if exist "%USERPROFILE%\Desktop" (
    echo @echo off > "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo echo Starting WiFi Login Tool (Headless)... >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo docker-compose up wifi-login-headless >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo pause >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo ✓ Desktop headless shortcut created
)

REM Create local shortcuts
echo @echo off > "WiFi Login Tool (CLI).bat"
echo echo Starting WiFi Login Tool... >> "WiFi Login Tool (CLI).bat"
echo docker-compose up wifi-login-cli >> "WiFi Login Tool (CLI).bat"
echo pause >> "WiFi Login Tool (CLI).bat"
echo ✓ Local CLI shortcut created (WiFi Login Tool (CLI).bat)

echo @echo off > "WiFi Login Tool (Headless).bat"
echo echo Starting WiFi Login Tool (Headless)... >> "WiFi Login Tool (Headless).bat"
echo docker-compose up wifi-login-headless >> "WiFi Login Tool (Headless).bat"
echo pause >> "WiFi Login Tool (Headless).bat"
echo ✓ Local headless shortcut created (WiFi Login Tool (Headless).bat)

echo @echo off > "WiFi Login Tool (GUI).bat"
echo echo Starting WiFi Login Tool (GUI)... >> "WiFi Login Tool (GUI).bat"
echo echo This will start the GUI version with VNC support. >> "WiFi Login Tool (GUI).bat"
echo echo Connect to VNC at localhost:5900 to access the GUI. >> "WiFi Login Tool (GUI).bat"
echo docker-compose up wifi-login-gui >> "WiFi Login Tool (GUI).bat"
echo pause >> "WiFi Login Tool (GUI).bat"
echo ✓ Local GUI shortcut created (WiFi Login Tool (GUI).bat)

echo.
echo Installation complete!
echo.
echo Usage:
echo   CLI version: docker-compose up wifi-login-cli
echo   Headless version: docker-compose up wifi-login-headless
echo   GUI version: docker-compose up wifi-login-gui
echo.
echo Or double-click the shortcuts:
echo   - WiFi Login Tool (CLI).bat
echo   - WiFi Login Tool (Headless).bat
echo   - WiFi Login Tool (GUI).bat
echo   - Desktop shortcuts (if created)
echo.
echo For GUI version: Connect to VNC at localhost:5900
echo For more information, see README.md and DOCKER.md
echo.
echo ⚠️  WARNING: Only use this tool on networks you trust!
pause 
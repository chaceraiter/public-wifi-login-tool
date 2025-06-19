@echo off
REM Public WiFi Login Tool - Portable Installation Script for Windows

echo Public WiFi Login Tool - Portable Installation
echo =============================================
echo.

REM Check if we're running from the correct directory
if not exist "scripts\wifi_login_tool.py" (
    echo ❌ Error: Please run this script from the WiFi_Login_Tool directory
    echo.
    echo Make sure you extracted the zip file and are running install_portable.bat
    echo from inside the extracted folder.
    pause
    exit /b 1
)

echo ✓ Found WiFi Login Tool scripts

REM Check if Python is already available
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✓ System Python detected - will use system Python
    set USE_SYSTEM_PYTHON=1
    goto :create_shortcuts
)

REM Check if portable Python exists
if exist "python\python.exe" (
    echo ✓ Portable Python detected
    set USE_SYSTEM_PYTHON=0
    goto :create_shortcuts
)

echo.
echo ❌ No Python found. This portable package requires Python to be included.
echo.
echo Please ensure you downloaded the complete portable package that includes
echo the Python runtime. The package should contain a 'python' folder.
echo.
echo If you have Python installed on your system, you can:
echo 1. Install Python from https://www.python.org/downloads/
echo 2. Or download the complete portable package
echo.
pause
exit /b 1

:create_shortcuts
echo.
echo Creating shortcuts...

REM Get current directory
set CURRENT_DIR=%CD%

REM Create desktop shortcuts
if exist "%USERPROFILE%\Desktop" (
    echo @echo off > "%USERPROFILE%\Desktop\WiFi Login Tool (GUI).bat"
    echo cd /d "%CURRENT_DIR%" >> "%USERPROFILE%\Desktop\WiFi Login Tool (GUI).bat"
    if "%USE_SYSTEM_PYTHON%"=="1" (
        echo python scripts\wifi_login_tool.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (GUI).bat"
    ) else (
        echo python\python.exe scripts\wifi_login_tool.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (GUI).bat"
    )
    echo pause >> "%USERPROFILE%\Desktop\WiFi Login Tool (GUI).bat"
    echo ✓ Desktop GUI shortcut created

    echo @echo off > "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo cd /d "%CURRENT_DIR%" >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    if "%USE_SYSTEM_PYTHON%"=="1" (
        echo python scripts\wifi_login_cli.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    ) else (
        echo python\python.exe scripts\wifi_login_cli.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    )
    echo pause >> "%USERPROFILE%\Desktop\WiFi Login Tool (CLI).bat"
    echo ✓ Desktop CLI shortcut created

    echo @echo off > "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo cd /d "%CURRENT_DIR%" >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    if "%USE_SYSTEM_PYTHON%"=="1" (
        echo python scripts\wifi_login_headless.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    ) else (
        echo python\python.exe scripts\wifi_login_headless.py >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    )
    echo pause >> "%USERPROFILE%\Desktop\WiFi Login Tool (Headless).bat"
    echo ✓ Desktop headless shortcut created
) else (
    echo ⚠ Desktop directory not found, skipping desktop shortcuts
)

REM Create local shortcuts
echo @echo off > "WiFi Login Tool (GUI).bat"
echo cd /d "%%~dp0" >> "WiFi Login Tool (GUI).bat"
if "%USE_SYSTEM_PYTHON%"=="1" (
    echo python scripts\wifi_login_tool.py >> "WiFi Login Tool (GUI).bat"
) else (
    echo python\python.exe scripts\wifi_login_tool.py >> "WiFi Login Tool (GUI).bat"
)
echo pause >> "WiFi Login Tool (GUI).bat"
echo ✓ Local GUI shortcut created

echo @echo off > "WiFi Login Tool (CLI).bat"
echo cd /d "%%~dp0" >> "WiFi Login Tool (CLI).bat"
if "%USE_SYSTEM_PYTHON%"=="1" (
    echo python scripts\wifi_login_cli.py >> "WiFi Login Tool (CLI).bat"
) else (
    echo python\python.exe scripts\wifi_login_cli.py >> "WiFi Login Tool (CLI).bat"
)
echo pause >> "WiFi Login Tool (CLI).bat"
echo ✓ Local CLI shortcut created

echo @echo off > "WiFi Login Tool (Headless).bat"
echo cd /d "%%~dp0" >> "WiFi Login Tool (Headless).bat"
if "%USE_SYSTEM_PYTHON%"=="1" (
    echo python scripts\wifi_login_headless.py >> "WiFi Login Tool (Headless).bat"
) else (
    echo python\python.exe scripts\wifi_login_headless.py >> "WiFi Login Tool (Headless).bat"
)
echo pause >> "WiFi Login Tool (Headless).bat"
echo ✓ Local headless shortcut created

echo.
echo Installation complete!
echo.
echo Usage:
echo   GUI version: Double-click "WiFi Login Tool (GUI).bat"
echo   CLI version: Double-click "WiFi Login Tool (CLI).bat"
echo   Headless version: Double-click "WiFi Login Tool (Headless).bat"
echo.
echo Or use the desktop shortcuts (if created)
echo.
echo ⚠️  WARNING: Only use this tool on networks you trust!
echo.
pause 
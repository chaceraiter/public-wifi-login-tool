@echo off
setlocal

:: Set paths relative to script location
set "INSTALL_DIR=%~dp0"
set "PYTHON_DIR=%INSTALL_DIR%python"
set "SHORTCUT_NAME=WiFi Login Tool.lnk"

echo Creating desktop shortcut...
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%USERPROFILE%\Desktop\%SHORTCUT_NAME%'); $SC.TargetPath = '%PYTHON_DIR%\pythonw.exe'; $SC.Arguments = 'launcher.py'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.IconLocation = '%INSTALL_DIR%\wifi.ico'; $SC.Save()"

:: Create autostart entry for headless service if configured
if exist "%INSTALL_DIR%config\headless.json" (
    echo Setting up autostart service...
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WiFi Login Service.lnk'); $SC.TargetPath = '%PYTHON_DIR%\pythonw.exe'; $SC.Arguments = 'launcher.py --headless'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.IconLocation = '%INSTALL_DIR%\wifi.ico'; $SC.Save()"
)

echo Installation complete!
echo You can now start the WiFi Login Tool from your desktop.
pause 
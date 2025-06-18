#!/bin/bash

# Public WiFi Login Tool - Installation Script

echo "Public WiFi Login Tool - Installation"
echo "====================================="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python $python_version detected"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✓ pip3 detected"

# Install dependencies
echo
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make scripts executable
echo
echo "Making scripts executable..."
chmod +x wifi_login_tool.py
chmod +x wifi_login_cli.py
chmod +x wifi_login_headless.py

echo "✓ Scripts made executable"

# Check if Chrome is installed (for GUI version)
if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
    echo "✓ Chrome/Chromium detected (for GUI version)"
else
    echo "⚠ Chrome/Chromium not detected. GUI version may not work properly."
    echo "  You can still use the CLI version."
fi

# Create shortcuts
echo
echo "Creating shortcuts..."

# Get current directory
CURRENT_DIR=$(pwd)

# Create desktop shortcut
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/WiFi Login Tool.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Login Tool
Comment=Access public WiFi login portals safely
Exec=python3 "$CURRENT_DIR/wifi_login_tool.py"
Icon=network-wireless
Terminal=false
Categories=Network;Utility;
EOF
    chmod +x "$HOME/Desktop/WiFi Login Tool.desktop"
    echo "✓ Desktop shortcut created"
else
    echo "⚠ Desktop directory not found, skipping desktop shortcut"
fi

# Create local shortcut
cat > "WiFi Login Tool.sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
python3 wifi_login_tool.py
EOF
chmod +x "WiFi Login Tool.sh"
echo "✓ Local shortcut created (WiFi Login Tool.sh)"

# Create CLI shortcut
cat > "WiFi Login CLI.sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
python3 wifi_login_cli.py
EOF
chmod +x "WiFi Login CLI.sh"
echo "✓ CLI shortcut created (WiFi Login CLI.sh)"

echo
echo "Installation complete!"
echo
echo "Usage:"
echo "  GUI version: python3 wifi_login_tool.py"
echo "  CLI version: python3 wifi_login_cli.py"
echo "  Or double-click the shortcuts:"
echo "    - WiFi Login Tool.sh (GUI)"
echo "    - WiFi Login CLI.sh (CLI)"
echo "    - Desktop shortcut (if created)"
echo
echo "For more information, see README.md"
echo
echo "⚠️  WARNING: Only use this tool on networks you trust!" 
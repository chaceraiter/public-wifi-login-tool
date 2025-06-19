#!/bin/bash

# Public WiFi Login Tool - Installation Script

echo "Public WiFi Login Tool - Installation"
echo "====================================="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo
    echo "Please install Docker:"
    echo "  Ubuntu/Debian: sudo apt-get install docker.io docker-compose"
    echo "  macOS: https://www.docker.com/products/docker-desktop"
    echo "  Other Linux: https://docs.docker.com/engine/install/"
    echo
    echo "After installation, add your user to the docker group:"
    echo "  sudo usermod -aG docker \$USER"
    echo "  Then log out and log back in."
    exit 1
fi

echo "✓ Docker detected"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo
    echo "Please start Docker and try again:"
    echo "  sudo systemctl start docker"
    echo "  Or start Docker Desktop (macOS/Windows)"
    exit 1
fi

echo "✓ Docker daemon is running"

# Build the Docker image
echo
echo "Building Docker image..."
if ! docker build -t wifi-login-tool .; then
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo "✓ Docker image built successfully"

# Create shortcuts
echo
echo "Creating shortcuts..."

# Get current directory
CURRENT_DIR=$(pwd)

# Create desktop shortcut for CLI version
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/WiFi Login Tool (CLI).desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Login Tool (CLI)
Comment=Access public WiFi login portals safely via CLI
Exec=gnome-terminal --working-directory="$CURRENT_DIR" -- docker-compose up wifi-login-cli
Icon=network-wireless
Terminal=true
Categories=Network;Utility;
EOF
    chmod +x "$HOME/Desktop/WiFi Login Tool (CLI).desktop"
    echo "✓ Desktop CLI shortcut created"
else
    echo "⚠ Desktop directory not found, skipping desktop shortcut"
fi

# Create desktop shortcut for headless version
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/WiFi Login Tool (Headless).desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Login Tool (Headless)
Comment=Access public WiFi login portals safely via headless browser
Exec=gnome-terminal --working-directory="$CURRENT_DIR" -- docker-compose up wifi-login-headless
Icon=network-wireless
Terminal=true
Categories=Network;Utility;
EOF
    chmod +x "$HOME/Desktop/WiFi Login Tool (Headless).desktop"
    echo "✓ Desktop headless shortcut created"
fi

# Create local shortcuts
cat > "WiFi Login Tool (CLI).sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
echo "Starting WiFi Login Tool (CLI)..."
docker-compose up wifi-login-cli
EOF
chmod +x "WiFi Login Tool (CLI).sh"
echo "✓ Local CLI shortcut created (WiFi Login Tool (CLI).sh)"

cat > "WiFi Login Tool (Headless).sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
echo "Starting WiFi Login Tool (Headless)..."
docker-compose up wifi-login-headless
EOF
chmod +x "WiFi Login Tool (Headless).sh"
echo "✓ Local headless shortcut created (WiFi Login Tool (Headless).sh)"

cat > "WiFi Login Tool (GUI).sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
echo "Starting WiFi Login Tool (GUI)..."
echo "This will start the GUI version with VNC support."
echo "Connect to VNC at localhost:5900 to access the GUI."
docker-compose up wifi-login-gui
EOF
chmod +x "WiFi Login Tool (GUI).sh"
echo "✓ Local GUI shortcut created (WiFi Login Tool (GUI).sh)"

echo
echo "Installation complete!"
echo
echo "Usage:"
echo "  CLI version: docker-compose up wifi-login-cli"
echo "  Headless version: docker-compose up wifi-login-headless"
echo "  GUI version: docker-compose up wifi-login-gui"
echo
echo "Or run the shortcuts:"
echo "  - ./WiFi Login Tool (CLI).sh"
echo "  - ./WiFi Login Tool (Headless).sh"
echo "  - ./WiFi Login Tool (GUI).sh"
echo "  - Desktop shortcuts (if created)"
echo
echo "For GUI version: Connect to VNC at localhost:5900"
echo "For more information, see README.md and DOCKER.md"
echo
echo "⚠️  WARNING: Only use this tool on networks you trust!" 
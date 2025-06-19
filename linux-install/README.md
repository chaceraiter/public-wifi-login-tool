# WiFi Login Tool - Linux Installation

This directory contains the Linux installation for the WiFi Login Tool using Docker containers.

## What is Docker Installation?

Docker provides a consistent, isolated environment that works the same on any Linux system. No need to install Python or dependencies on your system - everything runs in containers.

## Prerequisites

- Linux system (Ubuntu, Debian, CentOS, etc.)
- Docker Engine installed
- Docker Compose installed
- User added to docker group

## Installation

### 1. Install Docker (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and log back in
```

**CentOS/RHEL:**
```bash
sudo yum install docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Log out and log back in
```

### 2. Run the Installation Script

```bash
# Make script executable
chmod +x install.sh

# Run installation
./install.sh
```

The script will:
- Check if Docker is installed and running
- Build the Docker image
- Create shortcuts for all versions

## Usage

### CLI Version (Recommended)
```bash
# Auto-detect and access portal
docker-compose up wifi-login-cli

# Or use the shortcut
./WiFi Login Tool (CLI).sh
```

### Headless Version (Automated)
```bash
# Auto-detect with headless browser
docker-compose up wifi-login-headless

# Or use the shortcut
./WiFi Login Tool (Headless).sh
```

### GUI Version (with VNC)
```bash
# Start GUI version
docker-compose up wifi-login-gui

# Connect to VNC at localhost:5900
# Use any VNC client (RealVNC, TightVNC, etc.)

# Or use the shortcut
./WiFi Login Tool (GUI).sh
```

## Directory Structure

```
linux-install/
├── install.sh              # Installation script
├── docker/                 # Docker files
│   ├── Dockerfile          # Container definition
│   ├── docker-compose.yml  # Service definitions
│   └── DOCKER.md           # Detailed Docker guide
├── WiFi Login Tool (CLI).sh      # Created by installer
├── WiFi Login Tool (Headless).sh # Created by installer
├── WiFi Login Tool (GUI).sh      # Created by installer
└── README.md               # This file
```

## Docker Services

### wifi-login-cli
- Simple command-line interface
- Fastest option
- Opens portal in your default browser

### wifi-login-headless
- Automated browser access
- Can auto-submit forms
- Good for unattended use

### wifi-login-gui
- Full graphical interface
- Requires VNC client to access
- Most user-friendly option

## Advanced Usage

### Custom Portal URLs
```bash
# Run with specific URL
docker run --network host wifi-login-tool python wifi_login_cli.py -u http://portal.example.com

# Run headless with auto-submit
docker run --network host wifi-login-tool python wifi_login_headless.py -u http://portal.example.com --auto-submit
```

### Persistent Logs
```bash
# Create logs directory
mkdir logs

# Run with persistent logs
docker run --network host -v $(pwd)/logs:/app/logs wifi-login-tool
```

### Interactive Mode
```bash
# Run container interactively
docker run --network host -it wifi-login-tool bash

# Inside container, run any command
python wifi_login_cli.py --test
python wifi_login_headless.py --verbose
```

## Troubleshooting

### "Permission denied" Error
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

### "Docker daemon not running"
```bash
# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

### "Network host not supported"
```bash
# Use bridge networking instead
docker run wifi-login-tool python wifi_login_cli.py
```

### "No portal detected"
- Ensure you're connected to the WiFi network
- Try manual URL entry
- Check if the network uses a custom portal

## Security Considerations

### Container Security
- **Network Isolation**: Container uses host networking for portal access
- **No Persistent Storage**: Container doesn't store sensitive data
- **Non-root User**: Container runs as non-root user

### Network Security
- Only use on networks you trust
- Never enter sensitive information on public WiFi
- Use a VPN for additional security when possible

## Support

For detailed Docker usage instructions, see `docker/DOCKER.md`.

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure Docker is running: `docker info`
3. Check container logs: `docker logs <container_id>`
4. Try different network modes if host networking fails 
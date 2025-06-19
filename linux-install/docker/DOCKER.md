# Docker Usage Guide

This guide explains how to use the Public WiFi Login Tool in Docker containers.

## Why Docker?

Docker provides several advantages for this tool:

- **Consistent Environment**: Works the same on any system
- **Easy Installation**: No need to install Python, Chrome, or dependencies
- **Isolation**: Runs in a contained environment
- **Cross-Platform**: Works on Windows, Mac, and Linux
- **No Conflicts**: Doesn't interfere with your system's existing software

## Prerequisites

- **Docker Desktop** installed on your system
  - [Windows/Mac](https://www.docker.com/products/docker-desktop)
  - [Linux](https://docs.docker.com/engine/install/)

## Quick Start

### 1. Build the Container

```bash
# Build the Docker image
docker build -t wifi-login-tool .
```

### 2. Run the CLI Version

```bash
# Auto-detect and access portal
docker run --network host wifi-login-tool

# Test connectivity only
docker run --network host wifi-login-tool python wifi_login_cli.py --test

# Access specific URL
docker run --network host wifi-login-tool python wifi_login_cli.py -u http://portal.example.com
```

### 3. Run the Headless Version

```bash
# Auto-detect with headless browser
docker run --network host wifi-login-tool python wifi_login_headless.py

# With verbose output
docker run --network host wifi-login-tool python wifi_login_headless.py --verbose

# Access specific URL with auto-submit
docker run --network host wifi-login-tool python wifi_login_headless.py -u http://portal.example.com --auto-submit
```

## Using Docker Compose

Docker Compose makes it even easier to manage the containers:

### 1. Start CLI Service

```bash
# Run CLI version
docker-compose up wifi-login-cli

# Run in background
docker-compose up -d wifi-login-cli

# View logs
docker-compose logs wifi-login-cli
```

### 2. Start GUI Service (with VNC)

```bash
# Run GUI version with VNC
docker-compose up wifi-login-gui

# Connect to VNC at localhost:5900
# Use any VNC client (RealVNC, TightVNC, etc.)
```

### 3. Start Headless Service

```bash
# Run headless version
docker-compose up wifi-login-headless
```

## Advanced Usage

### Custom Portal URLs

```bash
# Run with custom URL
docker run --network host wifi-login-tool python wifi_login_cli.py -u http://192.168.1.1

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

## Windows-Specific Instructions

### PowerShell Commands

```powershell
# Build image
docker build -t wifi-login-tool .

# Run CLI version
docker run --network host wifi-login-tool

# Run with specific URL
docker run --network host wifi-login-tool python wifi_login_cli.py -u http://portal.example.com
```

### Windows Docker Desktop

1. **Enable WSL 2**: Make sure WSL 2 is enabled in Docker Desktop settings
2. **Network Mode**: Use `--network host` for better network access
3. **File Sharing**: Ensure your project directory is shared with Docker

### Alternative Network Mode

If `--network host` doesn't work on Windows:

```powershell
# Use bridge networking instead
docker run wifi-login-tool python wifi_login_cli.py --test
```

## Troubleshooting

### Common Issues

**"Network host not supported"**
```bash
# Use bridge networking instead
docker run wifi-login-tool python wifi_login_cli.py
```

**"Permission denied"**
```bash
# Run with sudo (Linux/Mac)
sudo docker run --network host wifi-login-tool

# Or add user to docker group
sudo usermod -aG docker $USER
```

**"Chrome failed to start"**
```bash
# This is normal in headless mode
# Check logs for actual errors
docker logs <container_id>
```

**"No portal detected"**
- Ensure you're connected to the WiFi network
- Try manual URL entry
- Check if the network uses a custom portal

### Debug Mode

```bash
# Run with debug output
docker run --network host wifi-login-tool python wifi_login_headless.py --verbose

# Check container logs
docker logs <container_id>
```

## Security Considerations

### Container Security

- **Network Isolation**: Container uses host networking for portal access
- **No Persistent Storage**: Container doesn't store sensitive data
- **Non-root User**: Container runs as non-root user
- **Temporary Files**: Screenshots and logs are temporary

### Usage Recommendations

1. **Only use on trusted networks**
2. **Don't enter sensitive information** in portal forms
3. **Use VPN** for additional security when possible
4. **Check portal URLs** before entering credentials
5. **Clean up containers** after use

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi wifi-login-tool

# Clean up all unused resources
docker system prune
```

## Performance Tips

### Optimize Container Size

```bash
# Use multi-stage build for smaller images
# (Already implemented in Dockerfile)

# Clean up after use
docker system prune -f
```

### Faster Startup

```bash
# Use volume mounts for persistent data
docker run -v $(pwd)/logs:/app/logs wifi-login-tool

# Use Docker Compose for easier management
docker-compose up wifi-login-cli
```

## Integration Examples

### Script Integration

```bash
#!/bin/bash
# Auto-connect to WiFi portal

echo "Connecting to WiFi portal..."

# Run container and capture output
PORTAL_URL=$(docker run --network host wifi-login-tool python wifi_login_cli.py -p 2>/dev/null | grep "Portal URL:" | cut -d' ' -f3)

if [ ! -z "$PORTAL_URL" ]; then
    echo "Opening portal: $PORTAL_URL"
    docker run --network host wifi-login-tool python wifi_login_headless.py -u "$PORTAL_URL" --auto-submit
else
    echo "No portal detected"
fi
```

### Cron Job

```bash
# Add to crontab for automatic portal detection
# */5 * * * * docker run --network host wifi-login-tool python wifi_login_cli.py --test
```

This Docker setup provides a robust, cross-platform solution for accessing WiFi login portals while maintaining security and ease of use. 
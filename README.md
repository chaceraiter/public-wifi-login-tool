# Public WiFi Login Tool

A safe tool to help access public WiFi login portals that browsers might block due to security restrictions.

## Problem

When connecting to public WiFi networks (hospitals, airports, hotels, etc.), you often encounter login portals that require you to accept terms, enter credentials, or provide information before gaining internet access. Modern browsers sometimes block these redirects, especially when they're HTTP (not HTTPS), making it difficult to access the login page.

## Solution

This tool provides multiple approaches to safely access these login portals:

1. **GUI Version** (`wifi_login_tool.py`) - A full graphical interface with network detection and controlled browser access
2. **CLI Version** (`wifi_login_cli.py`) - A simple command-line tool for quick portal detection and access
3. **Headless Version** (`wifi_login_headless.py`) - Container-optimized version for automated access
4. **Docker Container** - Cross-platform containerized solution (see [DOCKER.md](DOCKER.md))

## Features

### GUI Version
- **Network Status Detection**: Automatically detects your current network and connectivity status
- **Automatic Portal Detection**: Tries common portal URLs to find the login page
- **Manual URL Entry**: Enter specific portal URLs manually
- **Controlled Browser**: Opens portals in a Chrome browser with security settings optimized for portal access
- **Activity Logging**: Tracks all actions and provides detailed feedback
- **Safe Browsing**: Uses controlled browser settings to minimize security risks

### CLI Version
- **Quick Detection**: Fast portal detection without GUI overhead
- **Flexible Output**: Can open in browser or just print the URL
- **Connectivity Testing**: Tests internet access before attempting portal detection
- **Command-line Options**: Various options for different use cases

### Headless Version
- **Container Optimized**: Designed for Docker and automated environments
- **Screenshot Capture**: Takes screenshots of portal pages
- **Auto-submit Forms**: Attempts to automatically submit common form elements
- **Verbose Logging**: Detailed output for debugging

### Docker Container
- **Cross-Platform**: Works on Windows, Mac, and Linux
- **No Dependencies**: Everything included in the container
- **Easy Installation**: Just run the container, no setup required
- **Multiple Modes**: CLI, GUI (with VNC), and headless options

## Security Considerations

⚠️ **IMPORTANT**: This tool is designed for use on networks you trust. It intentionally bypasses some browser security restrictions.

### What This Tool Does Safely:
- Detects login portals using standard connectivity check URLs
- Opens portals in a controlled browser environment
- Provides clear warnings about security implications
- Uses standard HTTP requests for detection

### Security Risks to Be Aware Of:
- **Man-in-the-Middle Attacks**: Public WiFi networks can be compromised
- **Fake Portals**: Attackers might create fake login pages
- **Data Interception**: Traffic on public networks may be monitored
- **HTTP vs HTTPS**: Many portals use HTTP, which is not encrypted

### Recommendations:
1. **Only use on trusted networks** (airports, hospitals, known businesses)
2. **Never enter sensitive information** (banking, passwords) on public WiFi
3. **Use a VPN** for additional security when possible
4. **Be cautious of unexpected login pages**
5. **Check the URL** to ensure it matches the expected portal

## Installation

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop installed

**Quick Start:**
```bash
# Build the container
docker build -t wifi-login-tool .

# Run CLI version
docker run --network host wifi-login-tool

# Run headless version
docker run --network host wifi-login-tool python wifi_login_headless.py
```

For detailed Docker instructions, see [DOCKER.md](DOCKER.md).

### Option 2: Local Installation

**Prerequisites:**
- Python 3.7 or higher
- Chrome browser (for GUI version with controlled browser)

**Setup:**

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd public-wifi-login-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make scripts executable** (Linux/Mac)
   ```bash
   chmod +x wifi_login_tool.py
   chmod +x wifi_login_cli.py
   chmod +x wifi_login_headless.py
   ```

## Usage

### Docker Usage

**CLI Version:**
```bash
# Auto-detect and access portal
docker run --network host wifi-login-tool

# Test connectivity only
docker run --network host wifi-login-tool python wifi_login_cli.py --test

# Access specific URL
docker run --network host wifi-login-tool python wifi_login_cli.py -u http://portal.example.com
```

**Headless Version:**
```bash
# Auto-detect with headless browser
docker run --network host wifi-login-tool python wifi_login_headless.py

# With auto-submit
docker run --network host wifi-login-tool python wifi_login_headless.py --auto-submit
```

### Local Usage

**GUI Version:**
```bash
python wifi_login_tool.py
```

**CLI Version:**
```bash
# Basic usage
python wifi_login_cli.py

# Test connectivity only
python wifi_login_cli.py --test

# Open specific portal URL
python wifi_login_cli.py -u http://portal.example.com

# Print URL instead of opening browser
python wifi_login_cli.py -p
```

**Headless Version:**
```bash
# Auto-detect and access portal
python wifi_login_headless.py

# With verbose output
python wifi_login_headless.py --verbose

# Access specific URL with auto-submit
python wifi_login_headless.py -u http://portal.example.com --auto-submit
```

## How It Works

### Portal Detection
The tool tries common URLs that often trigger portal redirects:
- `http://captive.apple.com` (Apple devices)
- `http://www.msftconnecttest.com/redirect` (Windows)
- `http://connectivitycheck.gstatic.com/generate_204` (Android)
- `http://www.google.com/generate_204` (Google services)
- `http://1.1.1.1` and `http://8.8.8.8` (DNS servers)

When these URLs are accessed on a network with a login portal, they typically redirect to the portal page.

### Controlled Browser
The GUI and headless versions open portals in a Chrome browser with these settings:
- Disabled web security (allows HTTP redirects)
- Disabled extensions and plugins
- Custom user agent
- Disabled images (faster loading)
- No sandbox mode

## Troubleshooting

### Common Issues

**"No portal detected"**
- Ensure you're connected to the WiFi network
- Try manually entering the portal URL
- Some networks use custom portal URLs

**"Error opening controlled browser"**
- Ensure Chrome is installed (for local installation)
- Check if ChromeDriver is properly installed
- Try the CLI version instead
- Use Docker version for consistent environment

**"Browser security warnings"**
- This is expected behavior
- The tool intentionally bypasses some security restrictions
- Only use on trusted networks

**"Docker network issues"**
- Use `--network host` for better network access
- On Windows, try bridge networking if host mode doesn't work
- See [DOCKER.md](DOCKER.md) for detailed troubleshooting

### Manual Portal URLs

If auto-detection fails, try these common portal URLs:
- `http://192.168.1.1`
- `http://10.0.0.1`
- `http://172.16.0.1`
- `http://portal.example.com` (replace with actual network)

## Development

### Project Structure
```
public-wifi-login-tool/
├── wifi_login_tool.py      # GUI version
├── wifi_login_cli.py       # CLI version
├── wifi_login_headless.py  # Headless version
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
├── DOCKER.md              # Docker usage guide
├── install.sh             # Linux/Mac installation script
├── install.bat            # Windows installation script
└── README.md              # This file
```

### Dependencies
- `requests`: HTTP requests for portal detection
- `selenium`: Controlled browser automation
- `webdriver-manager`: ChromeDriver management
- `netifaces`: Network interface detection
- `psutil`: System and process utilities
- `tkinter`: GUI framework (usually included with Python)

## License

This project is provided as-is for educational and personal use. Use at your own risk and only on networks you trust.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Please ensure any changes maintain the security-focused approach of the tool.

## Disclaimer

This tool is designed to help access legitimate public WiFi login portals. Users are responsible for:
- Only using it on trusted networks
- Understanding the security implications
- Not using it for malicious purposes
- Complying with local laws and network policies

The authors are not responsible for any misuse or security incidents resulting from the use of this tool. 
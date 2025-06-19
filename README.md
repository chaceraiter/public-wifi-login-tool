# WiFi Login Tool

A secure tool to help users access public WiFi networks with captive portals. Perfect for corporate environments and situations where browsers block portal redirects.

## Key Features

- 🔒 Secure portal detection and access
- 🖥️ User-friendly GUI with system tray
- 🤖 Optional automated login service
- 🏢 Corporate environment friendly
- 📱 Works with most public WiFi networks
- 🛡️ No system modifications needed

## Quick Start

### Windows Users

1. Download `wifi-login-tool-portable.zip` from [Releases](../../releases)
2. Extract to any location (no installation needed)
3. Run `install.bat`
4. Use the desktop shortcut to start

Perfect for:
- Corporate laptops
- Systems with strict antivirus
- No admin rights needed
- Quick setup (1-2 clicks)

### Linux Users

1. Install Docker and Docker Compose
2. Clone or download this repository
3. Run:
   ```bash
   cd linux-install
   docker-compose up -d
   ```

The tool will appear in your system tray.

## Usage Guide

### Basic Usage

1. Connect to a WiFi network
2. Click the system tray icon
3. Click "Start Login Process"
4. Complete login in the opened browser

### Advanced Features

**Manual Portal URL**
- Enter specific portal URLs if auto-detection fails
- Useful for custom corporate portals

**Headless Mode**
- Automatic login for known networks
- Configure in `config/headless.json`
- See [Configuration Guide](docs/CONFIG.md)

## Security Features

- ✅ No system modifications
- ✅ Isolated browser environment
- ✅ No stored credentials (unless configured)
- ✅ Standard HTTP(S) requests only
- ✅ Clear security warnings
- ✅ Antivirus friendly

See [SECURITY.md](SECURITY.md) for details.

## Support

- 📖 [Configuration Guide](docs/CONFIG.md)
- 🛡️ [Security Policy](SECURITY.md)
- 🐛 [Issue Tracker](../../issues)
- 📧 [Security Contact](SECURITY.md#reporting-a-vulnerability)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

[MIT License](LICENSE) - Feel free to use and modify, but keep the license notice. 
# WiFi Login Tool - Windows Portable Installation

This directory contains the portable Windows installation for the WiFi Login Tool.

## What is Portable Installation?

The portable installation allows you to run the WiFi Login Tool without installing Python or any dependencies on your system. Everything needed is included in the package.

## Installation

### Prerequisites
- Windows 10 or later
- No Python installation required
- No admin rights required

### Quick Start

1. **Download** the portable package (zip file)
2. **Extract** to any folder on your computer
3. **Double-click** `install_portable.bat`
4. **Use the tool** by double-clicking the created shortcuts

### What Gets Installed

The installer creates shortcuts for three versions of the tool:

- **WiFi Login Tool (GUI).bat** - Full graphical interface
- **WiFi Login Tool (CLI).bat** - Command-line interface (fastest)
- **WiFi Login Tool (Headless).bat** - Automated browser version

## Directory Structure

```
WiFi_Login_Tool/
├── python/                    # Portable Python runtime
├── scripts/                   # WiFi Login Tool scripts
│   ├── wifi_login_tool.py     # GUI version
│   ├── wifi_login_cli.py      # CLI version
│   └── wifi_login_headless.py # Headless version
├── requirements/              # Python dependencies
├── chrome/                    # Portable Chrome (if included)
├── install_portable.bat       # Installation script
├── WiFi Login Tool (GUI).bat  # Created by installer
├── WiFi Login Tool (CLI).bat  # Created by installer
├── WiFi Login Tool (Headless).bat # Created by installer
└── README.md                  # This file
```

## Usage

### GUI Version (Recommended for most users)
- Double-click `WiFi Login Tool (GUI).bat`
- Provides a full graphical interface
- Shows network status and portal detection
- Opens login pages in a controlled browser

### CLI Version (Fastest)
- Double-click `WiFi Login Tool (CLI).bat`
- Quick portal detection
- Opens login page in your default browser
- Good for quick access

### Headless Version (Automated)
- Double-click `WiFi Login Tool (Headless).bat`
- Automated browser access
- Can attempt to auto-submit forms
- Good for unattended use

## Troubleshooting

### "Python not found" Error
- Make sure you downloaded the complete portable package
- The package should include a `python` folder
- If you have Python installed on your system, the tool will use it automatically

### "Chrome not found" Error
- The tool will use your system's Chrome browser
- Make sure Chrome is installed and up to date
- Some corporate environments may block Chrome access

### Antivirus Warnings
- The portable Python files may trigger antivirus software
- This is a false positive - the files are safe
- You may need to add the folder to your antivirus exclusions

### Network Access Issues
- Make sure you're connected to the WiFi network
- Some corporate networks block portal detection
- Try the CLI version for better compatibility

## Security Notes

⚠️ **IMPORTANT**: This tool is designed for use on networks you trust.

- Only use on networks you trust (airports, hospitals, known businesses)
- Never enter sensitive information on public WiFi
- The tool intentionally bypasses some browser security restrictions
- Use a VPN for additional security when possible

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Try a different version (GUI, CLI, or Headless)
3. Ensure you're connected to the WiFi network
4. Check that Chrome is installed and accessible

## Technical Details

### How It Works
- Uses portable Python runtime (no system installation)
- Detects captive portals using standard connectivity checks
- Opens portals in a controlled browser environment
- Provides safe access to login pages

### Dependencies
- Portable Python 3.7+ (included)
- Chrome browser (system installation)
- Network connectivity

### File Locations
- Scripts: `scripts/` directory
- Python: `python/` directory
- Dependencies: `requirements/` directory
- Shortcuts: Created in current directory and desktop 
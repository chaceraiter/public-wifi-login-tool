# Configuration Guide

This guide explains how to configure the WiFi Login Tool for different use cases.

## GUI Mode

The GUI mode requires minimal configuration. Just run the tool and it will:
- Detect portals automatically
- Show clear status messages
- Guide you through the login process

### Optional Settings

You can manually enter portal URLs if needed:
1. Open the main window from the system tray
2. Enter the URL in the "Portal URL" field
3. Click "Start Login Process"

## Headless Mode

Headless mode runs without user interaction, perfect for:
- Automated login to known networks
- Background service operation
- Scheduled reconnection

### Basic Configuration

Create `config/headless.json`:

```json
{
    "check_interval": 30,
    "max_attempts": 3,
    "portal_urls": [
        "http://portal.example.com"
    ]
}
```

- `check_interval`: Seconds between connection checks
- `max_attempts`: Login attempts before giving up
- `portal_urls`: Known portal URLs to try first

### Automated Login

For portals requiring credentials:

```json
{
    "check_interval": 30,
    "max_attempts": 3,
    "portal_urls": [
        "http://portal.example.com"
    ],
    "auto_login": {
        "enabled": true,
        "selectors": {
            "username": "#username-field",
            "password": "#password-field",
            "submit": "#login-button"
        },
        "credentials": {
            "username": "your_username",
            "password": "your_password"
        }
    }
}
```

⚠️ **Security Note**: Credentials are stored in plain text. Secure this file!

### Finding Selectors

To find the correct selectors:
1. Open the portal in Chrome
2. Right-click the field
3. Select "Inspect"
4. Look for `id` or unique `class` values
5. Use `#id` or `.class` format

Example selectors:
```json
{
    "username": "#login-form input[name='user']",
    "password": "#login-form input[type='password']",
    "submit": "#login-form button[type='submit']"
}
```

### Multiple Networks

Configure multiple networks:

```json
{
    "networks": [
        {
            "ssid": "Airport-WiFi",
            "portal_url": "http://airport.login",
            "auto_login": {
                "enabled": true,
                "selectors": {
                    "username": "#user",
                    "password": "#pass",
                    "submit": "#login"
                },
                "credentials": {
                    "username": "airport_user",
                    "password": "airport_pass"
                }
            }
        },
        {
            "ssid": "Hotel-Guest",
            "portal_url": "http://hotel.portal",
            "auto_login": {
                "enabled": true,
                "selectors": {
                    "username": "#guest-user",
                    "password": "#guest-pass",
                    "submit": ".login-button"
                },
                "credentials": {
                    "username": "room_number",
                    "password": "guest_code"
                }
            }
        }
    ]
}
```

### Advanced Options

```json
{
    "logging": {
        "level": "INFO",
        "file": "wifi_login.log",
        "max_size": 1048576,
        "backup_count": 3
    },
    "browser": {
        "timeout": 30,
        "user_agent": "Custom User Agent String",
        "window_size": [1024, 768]
    },
    "network": {
        "check_urls": [
            "http://connectivitycheck.gstatic.com/generate_204",
            "http://www.google.com/generate_204"
        ],
        "timeout": 5
    }
}
```

## Docker Configuration

### Environment Variables

Create `.env` file in `linux-install/`:

```bash
DISPLAY=:0                      # X11 display
CONFIG_PATH=/config/headless.json   # Config location
LOG_LEVEL=INFO                  # Logging detail
CHROME_ARGS=--no-sandbox        # Browser options
```

### Docker Compose

Customize `docker-compose.yml`:

```yaml
version: '3.8'
services:
  wifi-login-gui:
    environment:
      - DISPLAY=${DISPLAY}
      - CONFIG_PATH=${CONFIG_PATH}
      - LOG_LEVEL=${LOG_LEVEL}
    volumes:
      - ./config:/config
      - /tmp/.X11-unix:/tmp/.X11-unix
```

## Troubleshooting

### Common Issues

**Portal Not Detected**
- Check network connection
- Try manual URL entry
- Verify portal is accessible
- Check browser console for errors

**Auto-Login Fails**
- Verify selectors in DevTools
- Check credential format
- Look for portal changes
- Review log files

**Permission Issues**
- Check file permissions
- Verify Docker setup
- Review system logs
- Check user access

### Logs

Default log locations:
- Windows: `%USERPROFILE%\AppData\Local\wifi_login.log`
- Linux: `/var/log/wifi_login.log`
- Docker: `linux-install/logs/wifi_login.log` 
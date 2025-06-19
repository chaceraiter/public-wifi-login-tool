# Security Policy

## Supported Versions

Only the latest version is currently supported with security updates. We recommend always using the most recent release.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **DO NOT** create a public GitHub issue
2. Email: [INSERT_SECURITY_EMAIL]
3. Include detailed steps to reproduce
4. If possible, include proof of concept code

We'll acknowledge receipt within 24 hours and provide a detailed response within 72 hours.

## Security Considerations

### Data Privacy

1. **No Data Collection**
   - The tool does not collect or transmit any user data
   - No analytics or telemetry
   - No remote logging

2. **Local Storage**
   - Configuration files stored locally only
   - Credentials in headless mode stored in plain text (user's responsibility)
   - No browser data persistence between sessions

3. **Network Access**
   - Only connects to user-specified portals
   - Uses standard HTTP(S) requests for detection
   - No background network activity

### Browser Security

1. **Isolation**
   - Each session uses a fresh browser instance
   - No persistent cookies or cache
   - No extension loading
   - Sandboxed execution

2. **Portal Access**
   - Only accesses known portal detection URLs
   - User must manually approve unknown portals
   - Clear warning when accessing HTTP portals

### System Security

1. **Minimal Permissions**
   - No admin privileges required
   - No system modifications
   - No registry changes (Windows)
   - No system service installation

2. **Installation Security**
   - Portable installation (no system integration)
   - All files contained in one directory
   - Clean uninstallation (just delete directory)

3. **Dependencies**
   - All dependencies pinned to specific versions
   - No external package downloads during runtime
   - Self-contained Python environment

### Corporate Environment

1. **Network Policies**
   - Compatible with corporate proxies
   - No bypass of network security
   - Standard browser-based portal access

2. **Antivirus Compatibility**
   - No system hooks
   - No binary modifications
   - Clean Python source code
   - Official Python distribution

### Known Limitations

1. **Plain Text Credentials**
   - Headless mode configuration stores credentials in plain text
   - Users should secure access to configuration files
   - Not recommended for high-security environments

2. **HTTP Portal Access**
   - Some portals require HTTP access
   - Clear warnings provided
   - User must acknowledge risks

3. **Browser Automation**
   - Uses Selenium WebDriver
   - May be flagged by strict security policies
   - Alternative manual mode available

## Best Practices

### For Users

1. **Configuration Security**
   - Keep configuration files private
   - Don't share headless credentials
   - Use strong portal passwords
   - Regular credential rotation

2. **Network Safety**
   - Only use on trusted networks
   - Verify portal URLs
   - Use VPN when possible
   - Don't enter sensitive data

3. **Installation**
   - Download from official releases only
   - Verify checksums if provided
   - Keep tool updated
   - Review configuration files

### For Administrators

1. **Deployment**
   - Review source code before deployment
   - Test in isolated environment
   - Configure corporate proxy settings
   - Document approved usage

2. **Monitoring**
   - Monitor for unusual portal access
   - Review logs periodically
   - Track configuration changes
   - Update allowed portal lists

3. **Policy**
   - Define acceptable use policy
   - Document security exceptions
   - Maintain portal URL whitelist
   - Regular security reviews

## GitHub Security

1. **Repository Settings**
   - No sensitive data in repository
   - Branch protection enabled
   - Required reviews for changes
   - Automated security scanning

2. **Release Process**
   - Signed commits
   - Release checksums provided
   - Clear changelog
   - Security review before release

3. **Issue Tracking**
   - Security issues privately reported
   - No sensitive data in issues
   - Clear security policy
   - Responsible disclosure 
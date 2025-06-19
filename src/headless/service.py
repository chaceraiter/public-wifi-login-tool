"""
Headless service for automated WiFi login.
"""

import time
import logging
import signal
import sys
from typing import Optional, Dict, Any
import json
import os
from pathlib import Path

from ..core.portal import detect_portal, create_browser_session, check_internet_connectivity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("wifi_login.log")
    ]
)
logger = logging.getLogger(__name__)

class LoginService:
    """Service for automated WiFi login."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize service with optional config file."""
        self.running = False
        self.config = self.load_config(config_path)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        defaults = {
            "check_interval": 30,  # seconds
            "max_attempts": 3,
            "portal_urls": [],  # List of known portal URLs to try
            "auto_login": {
                "enabled": False,
                "selectors": {
                    "username": "",
                    "password": "",
                    "submit": ""
                },
                "credentials": {
                    "username": "",
                    "password": ""
                }
            }
        }
        
        if not config_path:
            return defaults
            
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {**defaults, **config}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return defaults
            
    def handle_signal(self, signum: int, frame: Any):
        """Handle termination signals."""
        logger.info("Received shutdown signal")
        self.running = False
        
    def try_auto_login(self, driver: Any, portal_url: str) -> bool:
        """Attempt automated login if configured."""
        if not self.config["auto_login"]["enabled"]:
            return False
            
        try:
            selectors = self.config["auto_login"]["selectors"]
            creds = self.config["auto_login"]["credentials"]
            
            # Find and fill username
            if selectors["username"] and creds["username"]:
                elem = driver.find_element("css selector", selectors["username"])
                elem.send_keys(creds["username"])
                
            # Find and fill password
            if selectors["password"] and creds["password"]:
                elem = driver.find_element("css selector", selectors["password"])
                elem.send_keys(creds["password"])
                
            # Find and click submit
            if selectors["submit"]:
                elem = driver.find_element("css selector", selectors["submit"])
                elem.click()
                
            return True
            
        except Exception as e:
            logger.error(f"Auto-login failed: {e}")
            return False
            
    def check_and_login(self) -> bool:
        """
        Check connection and attempt login if needed.
        Returns True if connected or login successful.
        """
        # Check current connectivity
        connected, status = check_internet_connectivity()
        if connected:
            return True
            
        logger.info("Connection check failed, attempting login...")
        
        # Try known portal URLs first
        for url in self.config["portal_urls"]:
            if self.try_portal_login(url):
                return True
                
        # Fall back to auto-detection
        return self.try_portal_login()
        
    def try_portal_login(self, url: Optional[str] = None) -> bool:
        """
        Attempt login through a specific portal or auto-detect.
        Returns True if login successful.
        """
        try:
            portal_url = url or detect_portal()
            if not portal_url:
                return False
                
            logger.info(f"Attempting login at: {portal_url}")
            driver = create_browser_session(headless=True)
            driver.get(portal_url)
            
            if self.try_auto_login(driver, portal_url):
                logger.info("Auto-login attempted")
            else:
                logger.warning("No auto-login configured")
                
            # Wait for connectivity
            max_attempts = 10
            for attempt in range(max_attempts):
                connected, _ = check_internet_connectivity()
                if connected:
                    driver.quit()
                    logger.info("Successfully connected!")
                    return True
                time.sleep(1)
                
            driver.quit()
            return False
            
        except Exception as e:
            logger.error(f"Portal login error: {e}")
            return False
            
    def run(self):
        """Run the service loop."""
        logger.info("Starting WiFi Login Service")
        self.running = True
        
        while self.running:
            if not self.check_and_login():
                logger.warning("Login attempt failed")
            
            # Wait before next check
            time.sleep(self.config["check_interval"])
            
        logger.info("Service stopped")

def main():
    """Main entry point for headless service."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="WiFi Login Service - Headless Mode",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file",
        type=str,
        default=None
    )
    
    args = parser.parse_args()
    
    service = LoginService(args.config)
    service.run()

if __name__ == "__main__":
    main() 
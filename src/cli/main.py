"""
Command-line interface for WiFi Login Tool.
"""

import sys
import time
import logging
import argparse
from typing import Optional

from ..core.portal import detect_portal, create_browser_session, check_internet_connectivity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_login_process(url: Optional[str] = None, headless: bool = False) -> bool:
    """
    Run the portal detection and login process.
    Returns True if login was successful.
    """
    try:
        # Check current connectivity
        connected, status = check_internet_connectivity()
        if connected:
            logger.info("Already connected to internet")
            return True
            
        logger.info("Detecting portal...")
        portal_url = detect_portal(url)
        
        if not portal_url:
            logger.error("No portal detected")
            return False
            
        logger.info(f"Opening portal page: {portal_url}")
        driver = create_browser_session(headless=headless)
        driver.get(portal_url)
        
        if not headless:
            logger.info("Please complete login in browser window")
        else:
            logger.info("Running in headless mode - waiting for auto-login")
        
        # Wait for connectivity
        max_attempts = 30
        for attempt in range(max_attempts):
            connected, _ = check_internet_connectivity()
            if connected:
                driver.quit()
                logger.info("Successfully connected!")
                return True
            logger.info(f"Waiting for connection... ({attempt + 1}/{max_attempts})")
            time.sleep(1)
        
        driver.quit()
        logger.error("Login timeout - please try again")
        return False
        
    except Exception as e:
        logger.error(f"Login process error: {e}")
        return False

def main():
    """Main entry point for CLI application."""
    parser = argparse.ArgumentParser(
        description="WiFi Login Tool - Command Line Interface",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-u", "--url",
        help="Optional portal URL to use instead of auto-detection",
        type=str,
        default=None
    )
    
    parser.add_argument(
        "--headless",
        help="Run in headless mode (no browser window)",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    success = run_login_process(args.url, args.headless)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
"""
Core portal detection and browser management functionality.
"""

import os
import sys
import time
import logging
import requests
from typing import Optional, Tuple, List
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Common portal detection URLs
PORTAL_CHECK_URLS = [
    "http://captive.apple.com",
    "http://www.msftconnecttest.com/redirect",
    "http://connectivitycheck.gstatic.com/generate_204",
    "http://www.google.com/generate_204",
    "http://1.1.1.1",
    "http://8.8.8.8"
]

def is_valid_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False

def check_internet_connectivity() -> Tuple[bool, str]:
    """Check current internet connectivity status."""
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return True, "Connected to internet"
        else:
            return False, "Limited connectivity"
    except requests.RequestException:
        return False, "No internet access"

def detect_portal(url: Optional[str] = None) -> Optional[str]:
    """
    Detect captive portal URL.
    If URL is provided, validates and returns it.
    Otherwise tries common portal detection URLs.
    """
    if url:
        return url if is_valid_url(url) else None

    for check_url in PORTAL_CHECK_URLS:
        try:
            logger.info(f"Trying {check_url}")
            response = requests.get(check_url, timeout=5, allow_redirects=True)
            
            # If we got redirected, we might have found the portal
            if response.history:
                final_url = response.url
                if is_valid_url(final_url) and final_url != check_url:
                    logger.info(f"Detected portal at: {final_url}")
                    return final_url
        except requests.RequestException as e:
            logger.debug(f"Error checking {check_url}: {e}")
            continue

    return None

def get_safe_chrome_options(headless: bool = False) -> Options:
    """
    Create safe Chrome options for portal access.
    Removes potentially dangerous flags and adds security-focused ones.
    """
    options = Options()
    
    # Security-focused options
    options.add_argument("--no-sandbox")  # Required for Docker/root
    options.add_argument("--disable-dev-shm-usage")  # Prevent crashes
    options.add_argument("--disable-extensions")  # No extensions needed
    options.add_argument("--disable-gpu")  # Better compatibility
    options.add_argument("--disable-software-rasterizer")  # Better compatibility
    
    if headless:
        options.add_argument("--headless=new")  # New headless mode
        
    # Privacy options
    options.add_argument("--incognito")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-notifications")
    
    # Performance options
    options.add_argument("--disable-animations")
    options.add_argument("--disable-smooth-scrolling")
    
    return options

def create_browser_session(headless: bool = False) -> webdriver.Chrome:
    """Create a new Chrome browser session with safe options."""
    options = get_safe_chrome_options(headless)
    service = Service(ChromeDriverManager().install())
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        logger.error(f"Failed to create browser session: {e}")
        raise 
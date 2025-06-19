#!/usr/bin/env python3
"""
Public WiFi Login Tool - Headless Version
Optimized for containerized environments and automated portal access.
"""

import requests
import time
import sys
import argparse
import json
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class HeadlessWiFiLogin:
    def __init__(self, headless=True, verbose=False):
        self.headless = headless
        self.verbose = verbose
        self.driver = None
        
    def log(self, message):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def test_connectivity(self):
        """Test internet connectivity"""
        self.log("Testing internet connectivity...")
        try:
            response = requests.get("http://httpbin.org/ip", timeout=5)
            if response.status_code == 200:
                self.log("✓ Connected to internet")
                return True
            else:
                self.log("⚠ Limited connectivity")
                return False
        except:
            self.log("✗ No internet access - may need login portal")
            return False
            
    def detect_portal(self):
        """Detect login portal automatically"""
        self.log("Detecting login portal...")
        
        portal_urls = [
            "http://captive.apple.com",
            "http://www.msftconnecttest.com/redirect",
            "http://connectivitycheck.gstatic.com/generate_204",
            "http://www.google.com/generate_204",
            "http://clients3.google.com/generate_204",
            "http://www.msftncsi.com/ncsi.txt",
            "http://www.apple.com/library/test/success.html",
            "http://1.1.1.1",
            "http://8.8.8.8",
        ]
        
        for url in portal_urls:
            try:
                if self.verbose:
                    self.log(f"  Trying {url}...")
                response = requests.get(url, timeout=5, allow_redirects=True)
                
                if response.status_code == 200:
                    final_url = response.url
                    if final_url != url:
                        self.log(f"✓ Detected redirect to: {final_url}")
                        return final_url
                    else:
                        if self.verbose:
                            self.log(f"  No redirect from {url}")
                        
            except requests.exceptions.RequestException as e:
                if self.verbose:
                    self.log(f"  Error with {url}: {e}")
                continue
        
        self.log("✗ No portal detected automatically")
        return None
        
    def setup_browser(self):
        """Setup headless Chrome browser"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Container-optimized settings
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            
            self.log("✓ Browser setup complete")
            return True
            
        except Exception as e:
            self.log(f"✗ Browser setup failed: {e}")
            return False
            
    def access_portal(self, url, auto_submit=False):
        """Access portal and optionally auto-submit"""
        if not self.driver:
            if not self.setup_browser():
                return False
                
        # Basic URL validation
        if not self._is_valid_url(url):
            self.log(f"Invalid URL: {url}")
            return False
                
        try:
            self.log(f"Accessing portal: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            self.log(f"Current URL: {current_url}")
            self.log(f"Page title: {page_title}")
            
            if auto_submit:
                self.auto_submit_form()
            
            # Keep browser open for manual interaction
            if not self.headless:
                self.log("Browser will remain open for manual interaction...")
                try:
                    self.driver.wait_for_quit()
                except:
                    pass
            else:
                # In headless mode, take screenshot and close
                screenshot_path = f"portal_screenshot_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                self.log(f"Screenshot saved: {screenshot_path}")
                self.driver.quit()
                
            return True
            
        except Exception as e:
            self.log(f"✗ Error accessing portal: {e}")
            if self.driver:
                self.driver.quit()
            return False
            
    def _is_valid_url(self, url):
        """Basic URL validation"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ('http', 'https') and parsed.netloc
        except:
            return False
            
    def auto_submit_form(self):
        """Attempt to auto-submit common form elements"""
        try:
            # Look for common submit buttons
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "button:contains('Accept')",
                "button:contains('Continue')",
                "button:contains('Login')",
                "button:contains('Connect')",
                ".accept-button",
                ".continue-button"
            ]
            
            for selector in submit_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        self.log(f"Found submit element: {selector}")
                        elements[0].click()
                        time.sleep(2)
                        return True
                except:
                    continue
                    
            self.log("No submit button found for auto-submission")
            return False
            
        except Exception as e:
            self.log(f"Error in auto-submit: {e}")
            return False
            
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def main():
    parser = argparse.ArgumentParser(
        description="Headless WiFi Login Tool - Container Optimized",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Auto-detect and access portal
  %(prog)s -u http://portal.example.com  # Access specific URL
  %(prog)s --no-headless      # Run with visible browser
  %(prog)s --auto-submit      # Try to auto-submit forms
  %(prog)s --verbose          # Show detailed output
        """
    )
    
    parser.add_argument("-u", "--url", 
                       help="Specific portal URL to access")
    parser.add_argument("--no-headless", action="store_true",
                       help="Run with visible browser (not headless)")
    parser.add_argument("--auto-submit", action="store_true",
                       help="Attempt to auto-submit forms")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed output")
    parser.add_argument("--test", action="store_true",
                       help="Only test connectivity")
    
    args = parser.parse_args()
    
    print("Public WiFi Login Tool - Headless Version")
    print("=" * 50)
    print("WARNING: Only use this tool on networks you trust!")
    print()
    
    tool = HeadlessWiFiLogin(
        headless=not args.no_headless,
        verbose=args.verbose
    )
    
    try:
        # Test connectivity
        has_internet = tool.test_connectivity()
        
        if args.test:
            return
            
        # Handle specific URL
        if args.url:
            tool.access_portal(args.url, args.auto_submit)
            return
            
        # Auto-detect portal
        portal_url = tool.detect_portal()
        
        if portal_url:
            tool.access_portal(portal_url, args.auto_submit)
        else:
            print("\nNo portal detected. You can try:")
            print("1. Manually entering the portal URL with -u option")
            print("2. Checking if you need to connect to the WiFi network first")
            
    finally:
        tool.cleanup()

if __name__ == "__main__":
    main() 
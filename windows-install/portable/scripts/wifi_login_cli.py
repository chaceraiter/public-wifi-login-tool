#!/usr/bin/env python3
"""
Public WiFi Login Tool - Command Line Version
A simple CLI tool to help access public WiFi login portals.
"""

import requests
import webbrowser
import time
import sys
import argparse
from urllib.parse import urlparse

def test_connectivity():
    """Test if we have internet connectivity"""
    print("Testing internet connectivity...")
    try:
        response = requests.get("http://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print("✓ Connected to internet")
            return True
        else:
            print("⚠ Limited connectivity")
            return False
    except:
        print("✗ No internet access - may need login portal")
        return False

def detect_portal():
    """Automatically detect login portal"""
    print("\nDetecting login portal...")
    
    # Common portal URLs that often trigger redirects
    portal_urls = [
        "http://captive.apple.com",
        "http://www.msftconnecttest.com/redirect",
        "http://connectivitycheck.gstatic.com/generate_204",
        "http://www.google.com/generate_204",
        "http://clients3.google.com/generate_204",
        "http://www.msftncsi.com/ncsi.txt",
        "http://www.apple.com/library/test/success.html",
        "http://1.1.1.1",  # Cloudflare DNS
        "http://8.8.8.8",  # Google DNS
    ]
    
    for url in portal_urls:
        try:
            print(f"  Trying {url}...")
            response = requests.get(url, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                final_url = response.url
                if final_url != url:
                    print(f"✓ Detected redirect to: {final_url}")
                    return final_url
                else:
                    print(f"  No redirect from {url}")
                    
        except requests.exceptions.RequestException as e:
            print(f"  Error with {url}: {e}")
            continue
    
    print("✗ No portal detected automatically")
    return None

def open_portal(url, method="browser"):
    """Open the portal URL"""
    print(f"\nOpening portal: {url}")
    
    if method == "browser":
        try:
            webbrowser.open(url)
            print("✓ Opened in default browser")
        except Exception as e:
            print(f"✗ Error opening browser: {e}")
    elif method == "print":
        print(f"Portal URL: {url}")
        print("Please open this URL in your browser manually.")

def main():
    parser = argparse.ArgumentParser(
        description="Public WiFi Login Tool - Access login portals safely",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Auto-detect and open portal
  %(prog)s -u http://portal.example.com  # Open specific URL
  %(prog)s -p                 # Print URL instead of opening browser
  %(prog)s --test             # Only test connectivity
        """
    )
    
    parser.add_argument("-u", "--url", 
                       help="Specific portal URL to open")
    parser.add_argument("-p", "--print-only", action="store_true",
                       help="Print URL instead of opening browser")
    parser.add_argument("--test", action="store_true",
                       help="Only test connectivity")
    
    args = parser.parse_args()
    
    print("Public WiFi Login Tool")
    print("=" * 50)
    print("WARNING: Only use this tool on networks you trust!")
    print("This tool bypasses some browser security restrictions.")
    print()
    
    # Test connectivity first
    has_internet = test_connectivity()
    
    if args.test:
        return
    
    # If we have internet, we probably don't need a portal
    if has_internet:
        print("\nYou appear to have internet access.")
        response = input("Do you still want to try to detect a login portal? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    # Handle specific URL
    if args.url:
        open_portal(args.url, "print" if args.print_only else "browser")
        return
    
    # Auto-detect portal
    portal_url = detect_portal()
    
    if portal_url:
        method = "print" if args.print_only else "browser"
        open_portal(portal_url, method)
        
        if method == "browser":
            print("\nIf the browser didn't open automatically, try:")
            print(f"  {portal_url}")
    else:
        print("\nNo portal detected. You can try:")
        print("1. Manually entering the portal URL with -u option")
        print("2. Checking if you need to connect to the WiFi network first")
        print("3. Looking for portal information from the network provider")

if __name__ == "__main__":
    main() 
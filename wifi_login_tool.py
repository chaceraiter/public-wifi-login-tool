#!/usr/bin/env python3
"""
Public WiFi Login Tool
A safe tool to help access public WiFi login portals that browsers might block.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
import time
import webbrowser
import socket
import subprocess
import platform
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import netifaces
import psutil

class WiFiLoginTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Public WiFi Login Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.check_network_status()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Public WiFi Login Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Network status section
        status_frame = ttk.LabelFrame(main_frame, text="Network Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Current Network:").grid(row=0, column=0, sticky=tk.W)
        self.network_label = ttk.Label(status_frame, text="Checking...", foreground="blue")
        self.network_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Label(status_frame, text="Connection Type:").grid(row=1, column=0, sticky=tk.W)
        self.connection_label = ttk.Label(status_frame, text="Checking...", foreground="blue")
        self.connection_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Manual URL section
        url_frame = ttk.LabelFrame(main_frame, text="Manual Login Portal Access", padding="10")
        url_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="Portal URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.url_entry.insert(0, "http://")
        
        url_buttons_frame = ttk.Frame(url_frame)
        url_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.open_browser_btn = ttk.Button(url_buttons_frame, text="Open in Browser", 
                                         command=self.open_portal_in_browser)
        self.open_browser_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_selenium_btn = ttk.Button(url_buttons_frame, text="Open in Controlled Browser", 
                                          command=self.open_portal_in_selenium)
        self.open_selenium_btn.pack(side=tk.LEFT)
        
        # Auto-detect section
        auto_frame = ttk.LabelFrame(main_frame, text="Automatic Detection", padding="10")
        auto_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.auto_detect_btn = ttk.Button(auto_frame, text="Detect and Open Login Portal", 
                                        command=self.auto_detect_portal)
        self.auto_detect_btn.pack()
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def check_network_status(self):
        """Check current network status"""
        def check_network():
            try:
                # Get default gateway
                gateways = netifaces.gateways()
                default_gateway = gateways['default'][netifaces.AF_INET][0]
                
                # Get network interface info
                interfaces = netifaces.interfaces()
                for interface in interfaces:
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        for addr_info in addrs[netifaces.AF_INET]:
                            ip = addr_info['addr']
                            if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                                self.network_label.config(text=f"{interface}: {ip}")
                                break
                
                # Test internet connectivity
                try:
                    response = requests.get("http://httpbin.org/ip", timeout=5)
                    if response.status_code == 200:
                        self.connection_label.config(text="Connected to Internet", foreground="green")
                    else:
                        self.connection_label.config(text="Limited connectivity", foreground="orange")
                except:
                    self.connection_label.config(text="No internet access - may need login", foreground="red")
                    
            except Exception as e:
                self.network_label.config(text="Error detecting network")
                self.connection_label.config(text="Unknown")
                self.log_message(f"Network detection error: {e}")
        
        threading.Thread(target=check_network, daemon=True).start()
        
    def auto_detect_portal(self):
        """Automatically detect and open the login portal"""
        def detect_portal():
            self.status_var.set("Detecting portal...")
            self.log_message("Starting automatic portal detection...")
            
            # Common portal URLs to try
            portal_urls = [
                "http://captive.apple.com",
                "http://www.msftconnecttest.com/redirect",
                "http://connectivitycheck.gstatic.com/generate_204",
                "http://www.google.com/generate_204",
                "http://clients3.google.com/generate_204",
                "http://www.msftncsi.com/ncsi.txt",
                "http://www.apple.com/library/test/success.html"
            ]
            
            for url in portal_urls:
                try:
                    self.log_message(f"Trying {url}...")
                    response = requests.get(url, timeout=5, allow_redirects=True)
                    
                    if response.status_code == 200:
                        # Check if we got redirected to a login page
                        final_url = response.url
                        if final_url != url:
                            self.log_message(f"Detected redirect to: {final_url}")
                            self.url_entry.delete(0, tk.END)
                            self.url_entry.insert(0, final_url)
                            self.open_portal_in_selenium()
                            return
                            
                except requests.exceptions.RequestException as e:
                    self.log_message(f"Error with {url}: {e}")
                    continue
            
            self.log_message("No portal detected automatically. Try manual URL entry.")
            self.status_var.set("No portal detected")
            
        threading.Thread(target=detect_portal, daemon=True).start()
        
    def open_portal_in_browser(self):
        """Open the portal URL in the default browser"""
        url = self.url_entry.get().strip()
        if not url or url == "http://":
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        # Basic URL validation
        if not self._is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        self.log_message(f"Opening {url} in default browser...")
        try:
            webbrowser.open(url)
            self.log_message("URL opened in default browser")
        except Exception as e:
            self.log_message(f"Error opening browser: {e}")
            messagebox.showerror("Error", f"Failed to open browser: {e}")
            
    def _is_valid_url(self, url):
        """Basic URL validation"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ('http', 'https') and parsed.netloc
        except:
            return False
            
    def open_portal_in_selenium(self):
        """Open the portal URL in a controlled Chrome browser"""
        url = self.url_entry.get().strip()
        if not url or url == "http://":
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        # Basic URL validation
        if not self._is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        def open_selenium():
            self.status_var.set("Opening controlled browser...")
            self.log_message(f"Opening {url} in controlled browser...")
            
            try:
                # Configure Chrome options for safe browsing
                chrome_options = Options()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-features=VizDisplayCompositor")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-plugins")
                chrome_options.add_argument("--disable-images")  # Optional: disable images for faster loading
                chrome_options.add_argument("--allow-running-insecure-content")  # Safer than disable-web-security
                chrome_options.add_argument("--ignore-certificate-errors")  # For self-signed certificates
                chrome_options.add_argument("--ignore-ssl-errors")  # For SSL issues
                
                # Add user agent to avoid detection
                chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                
                # Initialize the driver
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Set page load timeout
                driver.set_page_load_timeout(30)
                
                # Navigate to the URL
                driver.get(url)
                
                self.log_message("Controlled browser opened successfully")
                self.status_var.set("Browser opened")
                
                # Keep the browser open
                try:
                    driver.wait_for_quit()
                except:
                    pass
                    
            except Exception as e:
                self.log_message(f"Error opening controlled browser: {e}")
                self.status_var.set("Error opening browser")
                messagebox.showerror("Error", f"Failed to open controlled browser: {e}")
        
        threading.Thread(target=open_selenium, daemon=True).start()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("Public WiFi Login Tool")
    print("This tool helps access public WiFi login portals safely.")
    print("WARNING: Only use this tool on networks you trust.")
    print()
    
    app = WiFiLoginTool()
    app.run()

if __name__ == "__main__":
    main() 
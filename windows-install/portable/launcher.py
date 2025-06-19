"""
Launcher script for WiFi Login Tool.
This script is used by the Windows portable installation.
"""

import os
import sys
import argparse

# Add the src directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

def main():
    """Parse arguments and launch appropriate mode."""
    parser = argparse.ArgumentParser(description="WiFi Login Tool")
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    args = parser.parse_args()
    
    if args.headless:
        # Import and run headless service
        from src.headless.service import main as headless_main
        headless_main()
    else:
        # Import and run GUI
        from src.gui.app import main as gui_main
        gui_main()

if __name__ == "__main__":
    main() 
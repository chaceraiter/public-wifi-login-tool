"""
Build script for Windows portable package.
Creates a self-contained distribution with embedded Python.
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

# Configuration
PYTHON_VERSION = "3.11.8"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
PACKAGE_DIR = "portable"
PYTHON_DIR = os.path.join(PACKAGE_DIR, "python")

def download_file(url: str, target: str):
    """Download a file with progress indicator."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, target)

def create_directory_structure():
    """Create the required directory structure."""
    os.makedirs(PACKAGE_DIR, exist_ok=True)
    os.makedirs(PYTHON_DIR, exist_ok=True)
    os.makedirs(os.path.join(PACKAGE_DIR, "config"), exist_ok=True)
    os.makedirs(os.path.join(PACKAGE_DIR, "src"), exist_ok=True)

def download_and_extract_python():
    """Download and extract embedded Python."""
    python_zip = "python_embedded.zip"
    download_file(PYTHON_URL, python_zip)
    
    print("Extracting Python...")
    with zipfile.ZipFile(python_zip, 'r') as zip_ref:
        zip_ref.extractall(PYTHON_DIR)
    
    os.remove(python_zip)

def copy_project_files():
    """Copy project files to portable directory."""
    print("Copying project files...")
    
    # Copy source code
    shutil.copytree("../src", os.path.join(PACKAGE_DIR, "src"), dirs_exist_ok=True)
    
    # Copy launcher and install script
    shutil.copy("portable/launcher.py", PACKAGE_DIR)
    shutil.copy("portable/install.bat", PACKAGE_DIR)
    
    # Copy example config
    shutil.copy("../config/headless.example.json", 
                os.path.join(PACKAGE_DIR, "config", "headless.example.json"))
    
    # Copy icon
    shutil.copy("portable/wifi.ico", PACKAGE_DIR)

def install_dependencies():
    """Install Python dependencies into the embedded Python."""
    print("Installing dependencies...")
    pip_path = os.path.join(PYTHON_DIR, "python.exe")
    requirements = "../requirements.txt"
    
    subprocess.run([
        pip_path, "-m", "pip", "install",
        "-r", requirements,
        "--target", os.path.join(PYTHON_DIR, "Lib", "site-packages"),
        "--no-deps"  # Avoid system-wide installation
    ])

def create_zip():
    """Create the final ZIP package."""
    print("Creating ZIP package...")
    shutil.make_archive("wifi-login-tool-portable", "zip", PACKAGE_DIR)

def main():
    """Main build process."""
    print("Building Windows portable package...")
    
    # Ensure we're in the correct directory
    if not os.path.exists("portable"):
        print("Error: Must be run from windows-install directory")
        sys.exit(1)
    
    # Clean any existing build
    if os.path.exists(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)
    
    try:
        create_directory_structure()
        download_and_extract_python()
        copy_project_files()
        install_dependencies()
        create_zip()
        print("\nBuild complete! Package created as wifi-login-tool-portable.zip")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
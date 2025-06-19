"""
GUI application for WiFi Login Tool.
"""

import sys
import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QProgressBar,
    QMessageBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon

from ..core.portal import detect_portal, create_browser_session, check_internet_connectivity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PortalWorker(QThread):
    """Background worker for portal detection and login."""
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)
    
    def __init__(self, url: Optional[str] = None):
        super().__init__()
        self.url = url
        
    def run(self):
        """Run portal detection and login process."""
        try:
            # Check current connectivity
            connected, status = check_internet_connectivity()
            if connected:
                self.finished.emit(True, "Already connected to internet")
                return
                
            self.progress.emit("Detecting portal...")
            portal_url = detect_portal(self.url)
            
            if not portal_url:
                self.finished.emit(False, "No portal detected")
                return
                
            self.progress.emit("Opening portal page...")
            driver = create_browser_session()
            driver.get(portal_url)
            
            # Let user handle the login
            self.progress.emit("Please complete login in browser window")
            
            # Wait for connectivity
            max_attempts = 30
            for _ in range(max_attempts):
                connected, _ = check_internet_connectivity()
                if connected:
                    driver.quit()
                    self.finished.emit(True, "Successfully connected!")
                    return
                self.progress.emit("Waiting for connection...")
                self.sleep(1)
            
            driver.quit()
            self.finished.emit(False, "Login timeout - please try again")
            
        except Exception as e:
            logger.error(f"Portal worker error: {e}")
            self.finished.emit(False, f"Error: {str(e)}")

class MainWindow(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Login Tool")
        self.setFixedSize(400, 300)
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # URL input
        url_label = QLabel("Portal URL (optional):")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://...")
        
        # Progress bar and status
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        self.status_label = QLabel("Ready")
        
        # Buttons
        self.start_button = QPushButton("Start Login Process")
        self.start_button.clicked.connect(self.start_process)
        
        # Add widgets to layout
        layout.addWidget(url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        
        # System tray
        self.setup_tray()
        
    def setup_tray(self):
        """Setup system tray icon and menu."""
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon.fromTheme("network-wireless"))
        
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", self.close)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def start_process(self):
        """Start the portal detection and login process."""
        self.start_button.setEnabled(False)
        self.progress.setMaximum(0)  # Show busy indicator
        
        url = self.url_input.text().strip()
        url = url if url else None
        
        self.worker = PortalWorker(url)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.process_finished)
        self.worker.start()
        
    def update_status(self, message: str):
        """Update status message."""
        self.status_label.setText(message)
        
    def process_finished(self, success: bool, message: str):
        """Handle process completion."""
        self.progress.setMaximum(100)
        self.progress.setValue(100 if success else 0)
        self.status_label.setText(message)
        self.start_button.setEnabled(True)
        
        if success:
            self.tray.showMessage(
                "WiFi Login Tool",
                "Successfully connected to network",
                QSystemTrayIcon.MessageIcon.Information
            )
        else:
            QMessageBox.warning(self, "Login Failed", message)
            
    def closeEvent(self, event):
        """Handle window close event."""
        self.tray.hide()
        event.accept()

def main():
    """Main entry point for GUI application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 
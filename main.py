import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtCore import Qt, QTimer
from snipping import Snip
import keyboard  # For global key tracking
import threading  # For background thread to handle global key events
import time  # To use time.sleep()

class ScreenRegionSelector(QMainWindow):

    def __init__(self):
        super().__init__(None)
        self.m_width = 400
        self.m_height = 500

        self.setWindowTitle("Snip-Translator")
        self.setMinimumSize(self.m_width, self.m_height)

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel()
        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)

        self.btn_copy = QPushButton("Copy to Clipboard")
        self.btn_copy.clicked.connect(self.copy)
        self.btn_copy.setVisible(False)

        lay.addWidget(self.label)
        lay.addWidget(self.btn_capture)
        lay.addWidget(self.btn_copy)

        self.setCentralWidget(frame)

        # Set to track key presses
        self.pressed_keys = set()

        # Start global key listener
        keyboard.on_press(self.global_key_press)
        keyboard.on_release(self.global_key_release)

        # Flag to track whether the capture window is shown
        self.capturing = False

        # Start background thread to listen for Esc key globally
        self.app_is_running = True
        self.key_thread = threading.Thread(target=self.key_handler, daemon=True)
        self.key_thread.start()

        # Store the extracted text here
        self.extracted_text = ""

    def global_key_press(self, event):
        # Add the key to the set when pressed
        if event.name == '[':
            self.pressed_keys.add('[')
        elif event.name == ']':
            self.pressed_keys.add(']')

        # If both "[" and "]" are pressed, activate the capture
        if '[' in self.pressed_keys and ']' in self.pressed_keys:
            QTimer.singleShot(0, self.capture)
            self.pressed_keys.clear()  # Clear the set after triggering the capture

    def global_key_release(self, event):
        # Remove the key from the set when released
        if event.name == '[':
            self.pressed_keys.discard('[')
        elif event.name == ']':
            self.pressed_keys.discard(']')

    def capture(self):
        # Create and show the capture window
        self.capturer = Snip(self)
        self.capturer.show()
        self.capturing = True  # Indicate that capture is active

        self.btn_copy.setVisible(True)

    def copy(self):
        """Copy the extracted text to the clipboard"""
        if self.extracted_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.extracted_text)  # Set the clipboard to the extracted text
            print(f"Text copied to clipboard: {self.extracted_text}")
        else:
            print("No text to copy!")

    def close_capture_window(self):
        """Hide the capture window when Esc is pressed"""
        if self.capturer:
            self.capturer.hide()
        self.capturing = False  # Reset the capturing flag
        self.show()  # Show the main window again

    def key_handler(self):
        """Listen for the 'Esc' key globally in the background"""
        while self.app_is_running:
            if keyboard.is_pressed("esc"):  # Check if 'Esc' key is pressed
                self.close_capture_window()
            time.sleep(0.1)  # Use time.sleep() to prevent CPU overload


if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setStyleSheet("""
    QFrame {
        background-color: #3f3f3f;
    }
    QPushButton {
        border-radius: 5px;
        background-color: rgb(60, 90, 255);
        padding: 10px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
    QPushButton::hover {
        background-color: rgb(60, 20, 255)
    }
    """)
    selector = ScreenRegionSelector()
    selector.show()
    app.exit(app.exec_())

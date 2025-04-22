from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QMouseEvent, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
import os
import ocr  # Import the OCR module

class Snip(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.main.hide()

        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.15)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.end = QPoint()
        self.selection_rect = QRect()  # To store the selection region (top-left, bottom-right)

        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()

        # Removing time.sleep to optimize
        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(), rect.y(), rect.width(), rect.height()
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Trigger the close method in the main window (ScreenRegionSelector)
            self.main.close_capture_window()
            event.accept()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()  # Record the start point of the selection
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()  # Hide the rubber band after selection

            # Get the rectangle of the selected region
            self.selection_rect = self.rubber_band.geometry()

            # Update the image to reflect the selected region
            self.imgmap = self.imgmap.copy(self.selection_rect)

            QApplication.restoreOverrideCursor()  # Restore the cursor

            # Set clipboard
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.imgmap)

            self.main.label.setPixmap(self.imgmap)
            self.main.show()

            # Log the selection rectangle coordinates
            self.log_selection_range()

            # Save the snipped image temporarily to a file
            temp_file_path = "captured_snip.png"
            self.imgmap.save(temp_file_path)

            # Perform OCR on the saved image file
            text = ocr.read_text_from_image(temp_file_path)

            # Display the extracted text (optional, but not necessary since it will print to the console)
            self.main.label.setText(f"Extracted Text: {text}")

            # Delete the temporary snipped image file after processing
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  # Delete the snipped image file

            self.close()  # Close the capture window

            # Return the extracted text to the main window
            self.main.extracted_text = text  # Store the extracted text in the main window

    def log_selection_range(self):
        """Log the captured region's pixel coordinates (top-left and bottom-right)"""
        top_left = self.selection_rect.topLeft()
        bottom_right = self.selection_rect.bottomRight()

        print(f"Captured area:")
        print(f"Top-left: ({top_left.x()}, {top_left.y()})")
        print(f"Bottom-right: ({bottom_right.x()}, {bottom_right.y()})")

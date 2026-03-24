import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QLabel, QApplication

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.scale_factor = 1.0

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)
        self.adjustSize()  # Adjust the label size to fit the pixmap

    def wheelEvent(self, event: QWheelEvent):
        # Zoom in or out based on mouse wheel movement
        if event.angleDelta().y() > 0:
            self.scale_factor *= 1.1  # Zoom in
        else:
            self.scale_factor /= 1.1  # Zoom out

        # Apply the scaling to the pixmap
        self.resize(self.scale_factor * self.pixmap().size())
        self.setPixmap(self.pixmap())  # Update the pixmap with new size

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            # Calculate the new position based on mouse movement
            delta = event.pos() - self.last_mouse_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.last_mouse_pos = event.pos()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = ImageLabel()
    label.setPixmap(QPixmap('path_to_image.jpg'))  # You need to provide the image path
    label.resize(800, 600)
    label.show()
    sys.exit(app.exec_())
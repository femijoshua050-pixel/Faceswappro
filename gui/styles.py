import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

DARK_THEME = '''
QWidget {
    background-color: #121212;
    color: #E0E0E0;
}

QPushButton {
    background-color: #1E1E1E;
    color: #FFFFFF;
    border: none;
    padding: 10px;
}

QPushButton:hover {
    background-color: #3A3A3A;
}
'''


def apply_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
    palette.setColor(QPalette.Button, QColor(30, 30, 30))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    app.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_theme(app)
    # Your main window code goes here
    sys.exit(app.exec_())
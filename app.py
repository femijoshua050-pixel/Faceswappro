cat > app.py << 'EOF'
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
import warnings
import torch

warnings.filterwarnings('ignore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from gui.styles import apply_theme

class FaceSwapProApp:
    def __init__(self):
        self.setup_environment()
        self.app = QApplication(sys.argv)
        self.setup_app_style()
        self.window = MainWindow()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

    def setup_environment(self):
        directories = ['models', 'outputs', 'temp', 'face_db']
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def setup_app_style(self):
        self.app.setStyle('Fusion')
        apply_theme(self.app)

    def run(self):
        print("FaceSwapPro Application Started")
        self.window.show()
        return self.app.exec_()

if __name__ == '__main__':
    app = FaceSwapProApp()
    sys.exit(app.run())
EOF
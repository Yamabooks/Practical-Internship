import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定
        self.setWindowTitle('Image Display')
        self.setGeometry(100, 100, 800, 600)

        # QLabel を作成し、画像を表示
        label = QLabel(self)
        pixmap = QPixmap('images/zunda.png')  # ここに画像ファイルのパスを指定
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        # QLabel をウィンドウの中央に配置
        self.setCentralWidget(label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec())

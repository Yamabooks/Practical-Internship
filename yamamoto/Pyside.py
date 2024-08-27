import PySide6
from PySide6.QtWidgets import QApplication, QWidget
import os
import sys


# PySide6のアプリ本体（ユーザがコーディングしていく部分）
class MainWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None):    # parentは他にウィンドウを表示させる場合に指定する
        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化

        # ウィンドウ位置とサイズを指定
        xPos = 400 # x座標
        yPos = 200 # y座標
        windowWidth = 600 # 横幅
        windowHeight = 500 # 高さ
        self.setGeometry(xPos, yPos, windowWidth, windowHeight) # ウィンドウサイズの変更




        self.setWindowTitle("Pyside6で作ったアプリです。") # ウィンドウタイトル


if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了

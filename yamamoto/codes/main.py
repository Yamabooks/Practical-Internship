import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from time import sleep
import threading

from chatbot_client import ChatPlayer
#from voicevox_client1 import VoiceVoxClient
from voicevox_client2 import VoiceGenerator

def main():
    # オブジェクトの定義
    zunda1_path = 'yamamoto/codes/images/wait_zunda.gif'
    zunda2_path = 'yamamoto/codes/images/talk_zunda.gif'

    # GUIの基本ウィンドウを作成
    root = tk.Tk()
    root.title("Sample Application")

    # ここでウインドウサイズを定義する
    root.geometry('1200x600')

    # メインフレーム作成
    main_frame = tk.Frame(root, bg='lightblue')
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    # サブフレーム作成
    sub_frame = tk.Frame(root, bg='lightgreen')
    sub_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    # アニメーションを開始
    gif_player = TkGif(root, zunda1_path, zunda2_path, main_frame)
    gif_player.play()

    # Voicevox起動
    #voicevox = VoiceVoxClient() # オンライン用
    voicevox = VoiceGenerator() # オフライン用

    # カメラを起動してuser_idを取得
    user_id = "user999" # default

    # チャットボットを作成
    chat_player = ChatPlayer(root, sub_frame, voicevox, gif_player, user_id)

    root.mainloop()

# GIF
class GifPlayer(threading.Thread):
    def __init__(self, path1: str, path2: str, label: tk.Label):
        super().__init__(daemon=True)
        self._please_stop = False
        self.path1 = path1
        self.path2 = path2
        self.label = label
        self.duration = []  # フレーム表示間隔
        self.frames = []  # 読み込んだGIFの画像フレーム
        self.last_frame_index = None

        # フレームの読み込み
        self.load_frames2()

    # 残像なし
    def load_frames1(self):
        if isinstance(self.path1, str):
            img = Image.open(self.path1)
            frames = []

        frame_index = 0
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.copy()))
                frame_index += 1
                img.seek(frame_index)
        except EOFError:
            self.frames = frames
            self.last_frame_index = frame_index - 1

    # 残像あり
    def load_frames2(self):
        frames = []
        frame_index = 0
        try:
            while True:
                frames.append(tk.PhotoImage(file=self.path1, format=f'gif -index {frame_index}'))
                frame_index += 1
        except Exception:
            self.frames = frames
            self.last_frame_index = frame_index - 1

    def run(self):
        frame_index = 0
        while not self._please_stop:
            if self.frames:  # フレームが存在する場合のみ実行
                # インデックスが範囲内であることを確認
                if frame_index < len(self.frames):
                    self.label.after(0, self.label.configure, {'image': self.frames[frame_index]})
                    frame_index += 1
                else:
                    frame_index = 0  # フレーム数を超えたらリセット
            else:
                # フレームがない場合の対処（例えばログを出力するなど）
                print("No frames to display.")
            
            sleep(0.50)

    def stop(self):
        self._please_stop = True
    
    def update_gif(self, path):
        """GIFのパスを更新する"""
        self.path1 = path
        self.load_frames2()
    
    

class TkGif:
    def __init__(self, root, path1, path2, frame: tk.Frame) -> None:
        self.root = root
        self.path1 = path1
        self.path2 = path2
        self.frame = frame

        large_font = tkFont.Font(size=25)

        self.label = tk.Label(self.frame)
        self.label.pack(fill="x")
        self.txlabel = tk.Label(self.frame, text='', fg="lightgreen", font=large_font)  # テキスト挿入
        self.txlabel.pack(fill="x")

        self.player = GifPlayer(self.path1, self.path2, self.label)

    def play(self):
        self.player.start()

    def stop_loop(self):
        self.player.stop()
    
    def update_gif(self, path):
        self.player.update_gif(path)


if __name__ == "__main__":
    main()

from PIL import Image, ImageTk
import tkinter as tk
from time import sleep
import threading

class GifPlayer(threading.Thread):
    def __init__(self, path: str, label: tk.Label):
        super().__init__(daemon=True)
        self._please_stop = False
        self.path = path
        self.label = label
        self.duration = []  # フレーム表示間隔
        self.frames = []  # 読み込んだGIFの画像フレーム
        self.last_frame_index = None
        # フレームの読み込み
        self.load_frames2()

     # 残像がでない
    def load_frames1(self):
        if isinstance(self.path, str):
            img = Image.open(self.path)
            frames = []

        frame_index = 0
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(frame_index)
                frame_index += 1
        except EOFError:
            self.frames = frames
            self.last_frame_index = frame_index - 1

    # 残像がでる
    def load_frames2(self):
        frames = []
        frame_index = 0
        try:
            while True:
                frames.append(tk.PhotoImage(file=self.path, format=f'gif -index {frame_index}'))
                frame_index += 1
        except Exception:
            self.frames = frames
            self.last_frame_index = frame_index - 1

    def run(self):
        frame_index = 0
        while not self._please_stop:
            # configでフレーム変更
            self.label.configure(image=self.frames[frame_index])
            frame_index += 1
            # 最終フレームになったらフレームを０に戻す
            if frame_index > self.last_frame_index:
                frame_index = 0
            # 次のフレームまでの秒数
            sleep(0.06)

    def stop(self):
        self._please_stop = True


class TkGif():
    def __init__(self, path, label: tk.Label) -> None:
        self.path = path
        self.label = label

    def play(self):
        self.player = GifPlayer(self.path, self.label)
        self.player.start()

    def stop_loop(self):
        """loopを止める"""
        self.player.stop()


if __name__ == '__main__':

    path = './hoge.gif'

    root = tk.Tk()
    root.geometry('800x800')

    main_frame = tk.Frame(root)
    main_frame.pack()

    label = tk.Label(main_frame)
    label.pack()

    gif_player = TkGif(path, label)
    gif_player.play()

    root.mainloop()

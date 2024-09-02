import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import PhotoImage
import google.generativeai as genai
from PIL import Image, ImageTk
from time import sleep
import threading

def main():

    genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
    model = genai.GenerativeModel('gemini-pro')

    # オブジェクトの定義
    zunda1_path = './images/wait_zunda.gif'
    zunda2_path = './images/talk_zunda.gif'

    # GUIの基本ウィンドウを作成
    root = tk.Tk()
    root.title("Sample Application")

    # ここでウインドウサイズを定義する
    #root.geometry('800x600')

    # メインフレーム作成
    main_frame = tk.Frame(root, width=400, height=400)
    main_frame.pack(side=tk.LEFT, fill=tk.Y)

    gif_label = tk.Label()
    gif_label.pack()

    # アニメーションを開始
    gif_player = TkGif(zunda1_path, gif_label)
    gif_player.play()

    # サブフレーム作成
    sub_frame = tk.Frame(root, width=400, height=400)
    sub_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # ラベルを使って文字を画面上に出す
    Static1 = tk.Label(text=u'▼　Seriに話しかけよう!　▼')
    Static1.pack()

    # 入力ボックス
    entry = tk.Entry(width=50)
    entry.insert(tk.END, u'こんにちは')
    entry.pack()

    # ボタンを設置
    button = tk.Button(text = u'送信', width=50, command=lambda: addList(entry.get()))
    button.pack()

    # リストボックスを設置
    listbox = tk.Listbox(width=55, height=14)
    listbox.pack()

    root.mainloop()

# GIF
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
            sleep(0.40)

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


class chat_box():
    def __init__(self, text, listbox, entry, Seri, say , model):
        self.text = text
        self.listbox = listbox
        self.entry = entry
        self.Seri = Seri
        self.say = say
        self.model = model

    # ボタンが押されたらリストボックスに、Entryの中身を追加
    def addList(self):
        mysay = 'you: ' + self.text
        print(mysay)
        self.listbox.insert(tk.END, mysay)
        Seri = 'Seri: ' + self.talk(self.text)
        self.entry.delete(0, tk.END)
        self.addRep(Seri)

    def addRep(self):
        self.listbox.insert(tk.END, self.Seri)

    def talk(self): 
        if self.say == 'end':
            return('ではまた')
        else:
            response = self.model.generate_content(self.say)
            assistant_response = response.text
            return(assistant_response)


if __name__== "__main__":
    main()
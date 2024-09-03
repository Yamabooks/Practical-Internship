import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkm
import google.generativeai as genai
from PIL import Image, ImageTk
from time import sleep
import threading

from voicevox_client import VoiceVoxClient

def main():
    # オブジェクトの定義
    zunda1_path = './images/wait_zunda.gif'
    zunda2_path = './images/talk_zunda.gif'

    # GUIの基本ウィンドウを作成
    root = tk.Tk()
    root.title("Sample Application")

    # ここでウインドウサイズを定義する
    root.geometry('1000x600')

    # メインフレーム作成
    main_frame = tk.Frame(root, bg='lightblue')
    main_frame.pack(side=tk.LEFT, fill=tk.Y)

    # サブフレーム作成
    sub_frame = tk.Frame(root, bg='lightgreen')
    sub_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # アニメーションを開始
    gif_player = TkGif(root, zunda1_path, zunda2_path, main_frame)
    gif_player.play()

    # Voicevox起動
    client = VoiceVoxClient()

    # チャットボットを作成
    chat_player = ChatPlayer(root, sub_frame, client, gif_player)

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

    def load_frames1(self):
        if isinstance(self.path1, str):
            img = Image.open(self.path1)
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
            self.label.configure(image=self.frames[frame_index])
            frame_index += 1
            if frame_index > self.last_frame_index:
                frame_index = 0
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

        self.create_widget()

    def create_widget(self):
        self.label = tk.Label(
            self.frame,
            text='ずんだもんなのだ!'
            )
        self.label.pack()

    def play(self):
        self.player = GifPlayer(self.path1, self.path2, self.label)
        self.player.start()

    def stop_loop(self):
        self.player.stop()
    
    def update_gif(self, path):
        self.player.update_gif(path)

class ChatPlayer:
    def __init__(self, root, frame: tk.Frame, client, gif_player):
        self.root = root
        self.frame = frame
        self.client = client
        self.gif_player = gif_player

        genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
        self.model = genai.GenerativeModel('gemini-pro')

        self.create_widgets()

    def create_widgets(self):
        large_font = tkFont.Font(size=14)
        
        Static1 = tk.Label(self.frame, text=u'▼　Seriに話しかけよう!　▼', font=large_font)
        Static1.pack(pady=10)

        self.entry = tk.Entry(self.frame, width=60, font=large_font)
        self.entry.insert(tk.END, u'こんにちは')
        self.entry.pack(pady=10)

        self.button = tk.Button(self.frame, text=u'送信', width=60, height=2, font=large_font, command=self.on_send_button_click)
        self.button.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=65, height=20, font=large_font)
        self.listbox.pack(pady=10)

    def on_send_button_click(self):
        text = self.entry.get()
        if text.lower() in ['終了', 'exit']:
            self.root.quit()  # アプリケーションを終了
        else:
            self.entry.delete(0, tk.END)
            self.add_to_list(text)

    def add_to_list(self, text):
        mysay = 'you: ' + text
        print(mysay)
        self.listbox.insert(tk.END, mysay)
        
        # 送信中にボタンのテキストを変更し、無効化
        self.button.config(state=tk.DISABLED, text='生成中...')
        
        # 別スレッドで処理を実行
        threading.Thread(target=self.process_text, args=(text,)).start()

    def process_text(self, text):
        try:
            text = self.talk(text)
            Seri = 'Seri: ' + text
            print(Seri)
        except Exception as e:
            Seri = 'Seri: エラーが発生しました。'
            print(f"Error: {e}")
        
        self.add_response(text, Seri)

        # 処理が終わったらボタンを有効化
        self.root.after(0, self.button.config, {'state': tk.NORMAL, 'text': '送信'})

    def add_response(self, text, Seri):
        # 音声を作成
        wav = self.client.text_to_voice(text)
        # 音声再生前にGIFをpath2に切り替え
        self.gif_player.update_gif(self.gif_player.path2)
        # 文章を表示
        self.listbox.insert(tk.END, Seri)
        # 音声を再生
        self.client.play_wav(wav)
        sleep(0.50) # 時間を空ける
        # 音声再生後にGIFをpath1に戻す
        self.root.after(self.client.get_audio_duration(wav), self.gif_player.update_gif, self.gif_player.path1)



    def talk(self, say):
        if say == 'end':
            return 'ではまた'
        else:
            try:
                response = self.model.generate_content(say)
                assistant_response = response.text
                return assistant_response
            except Exception as e:
                tkm.showerror("エラー", f"応答を生成できませんでした: {str(e)}")
                return "よく聞き取れなかったのだ"

if __name__ == "__main__":
    main()

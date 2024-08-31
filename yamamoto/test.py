import tkinter as tk
from PIL import Image, ImageTk

# メインウィンドウを作成
root = tk.Tk()
root.title("Original Size Animated GIF Example")

# GIFのフレームを読み込む関数（サイズ変更なし）
def load_gif(filename):
    # PILを使用してGIFを開く
    gif = Image.open(filename)
    frames = []

    # 各フレームをTkinter用に変換
    for i in range(gif.n_frames):
        gif.seek(i)  # i番目のフレームを選択
        frame = gif.copy()  # フレームをコピー（オリジナルサイズのまま）
        tk_frame = ImageTk.PhotoImage(frame)  # Tkinter用に変換
        frames.append(tk_frame)

    return frames

# GIFのフレームを読み込み（サイズ変更なし）
frames = load_gif("./images/wait_zunda.gif")  # GIFファイルのパスを指定

# ラベルを作成
label = tk.Label(root)
label.pack()

# アニメーションを更新する関数
def update_frame(index):
    frame = frames[index]
    label.config(image=frame)
    index = (index + 1) % len(frames)  # 次のフレームに移動（ループ）
    root.after(300, update_frame, index)  # 200ミリ秒後に次のフレームに更新

# アニメーションを開始
update_frame(0)

# ウィンドウを表示
root.mainloop()

def main():
    import tkinter as tk
    from tkinter import ttk
    from tkinter import PhotoImage
    from PIL import Image, ImageTk # type: ignore

    # GUIの基本ウィンドウを作成
    root = tk.Tk()
    root.title("Sample Application")

    # オブジェクトの定義
    zunda_path = './images/zunda.png'
    zunda = Image.open(zunda_path)
    zunda = zunda.resize((300, 450), Image.LANCZOS)
    zunda = ImageTk.PhotoImage(zunda)

    label = ttk.Label(
        root,
        text="Hello, Tkinter!..なのだ", # テキスト
        foreground = '#1155ee', # テキストカラー
        padding = (10,15), # （左右、上下）パディング
        font = ('Times New Roman',20), # （フォント名、サイズ）
        wraplength = 400, # テキストの折り返しをピクセルで指定
        image = zunda,
        compound = 'left' # イメージ表示位置
        )
    entry = tk.Entry(root) # 入力ボックス
    button = tk.Button(root,text = 'OK') # ボタン

    # レイアウト
    label.pack()
    entry.pack()
    button.pack()

    # メインループを開始
    root.mainloop()

if __name__== "__main__":
    main()
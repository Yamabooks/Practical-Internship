def main():
    import tkinter as tk
    from tkinter import ttk
    from tkinter import PhotoImage
    import tkinter.messagebox as tkm
    import pya3rt
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
    
    # 入力ボックス
    lbl_entry = tk.Entry(width=50)
    lbl_entry.insert(tk.END, u'こんにちは')
    lbl_entry.pack()

    # ボタンを設置
    lbl_button = tk.Button(text = u'OK', width=50, command=lambda: addList(lbl_entry.get()))
    lbl_button.pack()

    # リストボックスを設置
    lbl_listbox = tk.lbl_listbox(width=55, height=14)

    # レイアウト
    label.pack()
    lbl_entry.pack()
    lbl_button.pack()
    lbl_listbox.pack()

    # メインループを開始
    root.mainloop()

        # ボタンが押されたらリストボックスに、Entryの中身を追加
    def addList(text):
        mysay = 'you: ' + text
        print(mysay)
        lbl_listbox.insert(tk.END, mysay)
        Seri = 'Seri: ' + talk(text)
        lbl_entry.delete(0, tk.END)
        addRep(Seri)

    def addRep(Seri):
        lbl_listbox.insert(tk.END, Seri)

    def talk(say):
        if say == 'end':
            return('ではまた')
        else:
            #ans_json = client.talk(say)
            #ans = ans_json['results'][0]['reply']
            return("なるほど")

if __name__== "__main__":
    main()
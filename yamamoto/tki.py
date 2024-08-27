def main():

    import sys
    import tkinter as tk
    import tkinter as ttk
    import tkinter.messagebox as tkm
    from tkinter import PhotoImage
    import pya3rt
    from PIL import Image, ImageTk
    import google.generativeai as genai

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
            response = model.generate_content(say)
            assistant_response = response.text
            return(assistant_response)

    genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
    model = genai.GenerativeModel('gemini-pro')

    # GUIの基本ウィンドウを作成
    root = tk.Tk()
    root.title("Sample Application")

    # ここでウインドウサイズを定義する
    #root.geometry('400x300')

    # オブジェクトの定義
    zunda_path = './images/zunda.png'
    zunda = Image.open(zunda_path)
    zunda = zunda.resize((300, 450), Image.LANCZOS)
    zunda = ImageTk.PhotoImage(zunda)

    label = ttk.Label(
        root,
        text="Hello, Tkinter!..なのだ", # テキスト
        foreground = '#1155ee', # テキストカラー
        font = ('Times New Roman',20), # （フォント名、サイズ）
        wraplength = 400, # テキストの折り返しをピクセルで指定
        image = zunda,
        compound = 'top' # イメージ表示位置
        )
    label.pack(side=tk.LEFT, padx=10)

    # ラベルを使って文字を画面上に出す
    Static1 = tk.Label(text=u'▼　Seriに話しかけよう!　▼')
    Static1.pack()

    # 入力ボックス
    lbl_entry = tk.Entry(width=50)
    lbl_entry.insert(tk.END, u'こんにちは')
    lbl_entry.pack()

    # ボタンを設置
    lbl_button = tk.Button(text = u'送信', width=50, command=lambda: addList(lbl_entry.get()))
    lbl_button.pack()

    # リストボックスを設置
    lbl_listbox = tk.Listbox(width=55, height=14)
    lbl_listbox.pack()

    root.mainloop()


if __name__== "__main__":
    main()
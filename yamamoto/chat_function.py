import sys
import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import PhotoImage
from PIL import Image, ImageTk
import google.generativeai as genai

class ChatPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sample Application")

        # Initialize generative model
        genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
        self.model = genai.GenerativeModel('gemini-pro')

        # Define GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Set up the window size
        # self.root.geometry('400x300')

        # Load and set the image
        zunda_path = './images/talk_zunda.gif'
        self.zunda = tk.PhotoImage(file=zunda_path)

        label = tk.Label(
            self.root,
            text="Hello, Tkinter!..なのだ",  # Text
            image=self.zunda,
            compound='top'  # Image display position
        )
        label.pack(padx=10)

        # Label for instructions
        Static1 = tk.Label(text=u'▼　Seriに話しかけよう!　▼')
        Static1.pack()

        # Input box
        self.lbl_entry = tk.Entry(width=50)
        self.lbl_entry.insert(tk.END, u'こんにちは')
        self.lbl_entry.pack()

        # Send button
        lbl_button = tk.Button(text=u'送信', width=50, command=self.on_send_button_click)
        lbl_button.pack()

        # Listbox for chat history
        self.lbl_listbox = tk.Listbox(width=55, height=14)
        self.lbl_listbox.pack()

    def on_send_button_click(self):
        text = self.lbl_entry.get()
        self.add_to_list(text)

    def add_to_list(self, text):
        mysay = 'you: ' + text
        print(mysay)
        self.lbl_listbox.insert(tk.END, mysay)
        Seri = 'Seri: ' + self.talk(text)
        self.lbl_entry.delete(0, tk.END)
        self.add_response(Seri)

    def add_response(self, Seri):
        self.lbl_listbox.insert(tk.END, Seri)

    def talk(self, say):
        if say == 'end':
            return 'ではまた'
        else:
            try:
                # Chatbotの応答を生成する部分
                response = self.model.generate_content(say)
                assistant_response = response.text
                return assistant_response
            except Exception as e:
                # エラーが発生した場合、メッセージボックスでエラーを表示
                tkm.showerror("エラー", f"応答を生成できませんでした: {str(e)}")
                return "エラーが発生しました。もう一度お試しください。"

def main():
    # Create the main window
    root = tk.Tk()

    # Instantiate the ChatPlayer class with the root window
    app = ChatPlayer(root)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()

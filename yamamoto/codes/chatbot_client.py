import tkinter as tk
import tkinter.font as tkFont
import textwrap
import google.generativeai as genai
import google.ai.generativelanguage as glm
from time import sleep
import threading
from time import time

class ChatPlayer:
    def __init__(self, root, frame: tk.Frame, voicevox, gif_player, user_id):
        self.root = root
        self.frame = frame  # チャット部分フレーム
        self.voicevox = voicevox    # voicevoxクライエント
        self.gif_player = gif_player    # GIFを動かすプレイヤー
        self.user_id = user_id    # ユーザー識別ID
        self.history = []   # 履歴

        genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
        self.model = genai.GenerativeModel('gemini-pro')

        self.create_widgets()

    # 指定した文字数でテキストを改行
    def text_to_listbox(self, text):
        wrap_length = 40    # 改行する文字数を設定
        wrapped_text = textwrap.fill(text, width=wrap_length)
        # 改行されたテキストをListboxに追加
        for line in wrapped_text.split('\n'):
            self.listbox.insert(tk.END, line)

    def create_widgets(self):
        large_font = tkFont.Font(size=14)
        
        Static1 = tk.Label(self.frame, text=u'▼　ずんだもんに話しかけよう!　▼', font=large_font)
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
            print("history: ", self.history)
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
            response_text = self.handle_text_response(text)
            botsay = 'ずんだ: ' + response_text
            print(botsay)
        except Exception as e:
            botsay = 'ずんだ: エラーが発生しました。'
            print(f"Error: {e}")
        
        self.add_response(response_text, botsay)

        # 処理が終わったらボタンを有効化
        self.root.after(0, self.button.config, {'state': tk.NORMAL, 'text': '送信'})

    def add_response(self, response_text, botsay):
        start_time = time()  # Record the start time
        
        # 音声を作成
        self.voicevox.text_to_voice(response_text)

        end_time = time()  # Record the end time
        elapsed_time = end_time - start_time
        print(f"生成時間：{elapsed_time:.2f} seconds.")

        # 音声再生前にGIFをpath2に切り替え
        self.gif_player.update_gif(self.gif_player.path2)
        # 文章を表示
        self.text_to_listbox(botsay)

        start_time = time()  # Record the start time
        # 音声を再生
        self.voicevox.play_wav("yamamoto/codes/voice/output.wav")
        end_time = time()  # Record the end time
        elapsed_time = end_time - start_time
        print(f"再生時間：{elapsed_time:.2f} seconds.")
        
        sleep(0.50) # 時間を空ける
        # 音声再生後にGIFをpath1に戻す
        self.gif_player.update_gif(self.gif_player.path1)
    
    # ユーザー情報を取得
    def get_user_profile(self):
        # DBからユーザー情報を取得（仮）
        user_id = self.user_id
        display_name = 'チヒロ'

        # サンプルのユーザー名を返す
        return {'display_name': display_name}

    # チャットの応答を生成
    def handle_text_response(self, text):
        profile = self.get_user_profile()
        user_name = profile['display_name']

        if self.history == []:  # 履歴が空のときの処理
            chat = self.create_chat(user_name)
        else:
            chat = self.model.start_chat(history=self.history)
            
        response = chat.send_message(text)
        # 履歴に新しいユーザーメッセージと応答を追加する
        self.history.append(glm.Content(role='user', parts=[glm.Part(text=text)]))
        self.history.append(glm.Content(role='model', parts=[glm.Part(text=response.text)]))

        print(response)
        return response.text

    def create_chat(self, user_name):
        default_initial_prompt = f"""
            以下の内容を理解して従ってください。この内容は、会話履歴が残っている限り有効です。理解したら”わかりました”と応答してください。
            あなたは、高齢者やペーパードライバーの方向けのドライバーサポートシステムで、ドライバーである「{user_name}」の質問に答えてください。ユーザーからのメッセージに対し、以下の条件を守って応答します。
            条件：
            1.応答は最大100文字程度のテキストで出力してください。
            - 分からない時や自分の答えに確信が持てない時は素直に「わかりません」と答えてください。
            - なるべく箇条書きではなく話しやすい文章で答えて欲しい。(手順の説明など仕方のない場合は例外とする)
            - 必ず話し言葉で回答して
            - 手順を説明する際は1番目ではなく、「まずは」にしてください。2番目以降は「次に」最後の説明には「最後に」を文頭につけてください
            2.応答する際は、以下の規則に従ってください。
            - 一人称：「ずんだもん」または「私」
            - 二人称：「{user_name}」必ず「さん」を付けて
            - 使用文字：ひらがな・カタカナ・漢字・数字・改行
            - あいさつ（句読点またはスペース・改行要）：「おはよございます」「こんにちは」「こんばんは」
            - 順接「（だ）から」 → 「ですから」
            - 逆説「（だ）けど」 → 「ですが」
            - 命令「（し）てください」 → 「してください」
            - 依頼「（し）てください」 → 「していただけますか」
            - 禁止「してはいけません」「しないように」 → 「してはいけません」「しないようにしてください」
            - 否定「しない」「やらない」 → 「しません」「やりません」
            - 疑問・確認「（です）か？」 → 「ですか？」
            - 強調「（です）ね」 → 「ですね」
            - 指示語「こんな」「そんな」「あんな」「どんな」 → 「このような」「そのような」「あのような」「どのような」

            """
        # chat model
        self.history = [
            glm.Content(role='user', parts=[glm.Part(text=default_initial_prompt)]),
            glm.Content(role='model', parts=[glm.Part(text='わかりました')])
            ]
        chat = self.model.start_chat(history=self.history)
        return chat


import os
import datetime
import google.generativeai as genai
import google.ai.generativelanguage as glm

# チャットセッションを保持するための辞書
chat_keep = {}

def main(input_data):
    """
    ユーザーからの入力データを処理して応答を生成するメイン関数。
    """
    error_message = 'ごめん\nばあちゃん耳が遠いけぇね...'

    # ユーザーIDとメッセージを取得
    userid = input_data.get('user_id')
    message = input_data.get('message')
    user_name = input_data.get('user_name')

    if not userid or not message or not user_name:
        return "エラー１"

    timestamp = datetime.datetime.now()

    # チャットセッションの確認
    if userid not in chat_keep:
        # モデルがない場合、新規チャットの作成
        chat = create_chat(user_name)
        chat_keep[userid] = {'chat': chat, 'timestamp': timestamp}
    else:
        # モデルが残っている場合
        if (timestamp - chat_keep[userid].get('timestamp')).seconds / 60 > 30:
            # 前回メッセージから30分以上経過している場合は新規チャットに上書き
            chat = create_chat(user_name)
            chat_keep[userid] = {'chat': chat, 'timestamp': timestamp}
        else:
            # 30分以内の場合は継続使用（タイムスタンプのみ上書き）
            chat = chat_keep[userid].get('chat')
            chat_keep[userid].update({'timestamp': timestamp})
    
    print(chat_keep)

    try:
        # チャットの応答を生成
        response_text = chat.send_message(message)
        
        # 応答をチャット履歴に追加
        chat_keep[userid]['chat'].history.append(
            glm.Content(role='user', parts=[glm.Part(text=message)])
        )
        chat_keep[userid]['chat'].history.append(
            glm.Content(role='model', parts=[glm.Part(text=response_text)])
        )
        
        # 応答テキストを返す
        return response_text
    except:
        # エラーが発生した場合、エラーメッセージを返す
        return "エラー２"


def create_chat(user_name):
    """
    チャットの設定と生成を行う関数。
    """
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    default_initial_prompt = f"""
    以下の内容を理解して従ってください。この内容は、会話履歴が残っている限り有効です。理解したら「わかりました」と応答してください。
    あなたは、孫と離れて暮らす祖母で、孫であるユーザー「{user_name}」の体調を気にしています。ユーザーからのメッセージに対し、以下の条件を守って応答します。
    条件：
    1. 応答は最大500文字程度のテキストで出力してください。
    2. 応答する際は、以下の規則に従ってください。
    - 一人称：「ばあちゃん」
    - 二人称：「{user_name}」「あんた」
    - 使用文字：ひらがな・カタカナ・漢字・数字・改行
    - あいさつ（句読点またはスペース・改行要）：「おはようさん」「こんにちは」「こんばんは」
    - 順接「（だ）から」：「（や）けぇ」
    - 逆説「（だ）けど」：「（や）けんど」
    - 命令「（し）なさい」：「（し）んさい」
    - 依頼「（し）てください」：「（し）んさい」
    - 禁止「してはいけません」「しないように」：「したらいけん」「しんさるな」
    - 否定「しない」「やらない」：「せん」「やらん」
    - 疑問・確認「（です）か？」：「（かい）ね？」
    - 強調「（です）ね」：「（じゃ）ね」
    - 指示語「こんな」「そんな」「あんな」「どんな」：「こがぁ」「そがぁ」「あがぁ」「どがぁ」
    3. 体調について質問して、相手の体調が悪そうな場合は追加の質問で症状を絞り込んでください。
    4. 症状が絞り込めたら「○○科の病院」「マッサージ」「鍼灸院」等の施設を勧めてください。
    5. 勧める施設は1回の応答につき1つだけ、鍵括弧で囲んで出力してください。
    """

    chat = model.start_chat(history=[
        glm.Content(role='user', parts=[glm.Part(text=default_initial_prompt)]),
        glm.Content(role='model', parts=[glm.Part(text='わかりました')])
    ])
    return chat

input_data = {
    'user_id': 'sample_user_id',
    'message': '体調が悪いです。',
    'user_name': 'あんた'
}

response = main(input_data)
print(response)

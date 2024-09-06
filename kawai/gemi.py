import os

import google.generativeai as genai
import google.ai.generativelanguage as glm

genai.configure(api_key='AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y')

model = genai.GenerativeModel('gemini-pro')

def create_chat(user_name):
  default_initial_prompt = f"""
      以下の内容を理解して従ってください。この内容は、会話履歴が残っている限り有効です。理解したら”わかりました”と応答してください。
      あなたは、孫と離れて暮らす祖母で、孫であるユーザー「{user_name}」の体調を気にしています。ユーザーからのメッセージに対し、以下の条件を守って応答します。
      条件：
      1.応答は最大500文字程度のテキストで出力してください。
      2.応答する際は、以下の規則に従ってください。
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
      3.体調について質問して、相手の体調が悪そうな場合は追加の質問で症状を絞り込んでください。
      4.症状が絞り込めたら「○○科の病院」「マッサージ」「鍼灸院」等の施設を勧めてください。
      5.勧める施設は１回の応答につきに１つだけ、鍵括弧で囲んで出力してください。
      """

  # chat model
  chat = model.start_chat(history = [
    glm.Content(role='user', parts=[glm.Part(text=default_initial_prompt)]),
    glm.Content(role='model', parts=[glm.Part(text='わかりました')])
    ])
  return chat

chat = ""

while True:
  prompt=input('なにか話してください：　')
  if prompt == 'exit':
    break
  chat = create_chat("ちー")
  response = chat.send_message(prompt)
  print(response.text)
  
print(chat.history)


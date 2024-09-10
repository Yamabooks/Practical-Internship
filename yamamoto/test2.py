import enum
import google.generativeai as genai
import os

# 列挙型の定義
class Choice(enum.Enum):
    PERCUSSION = "Percussion"
    STRING = "String"
    WOODWIND = "Woodwind"
    BRASS = "Brass"
    KEYBOARD = "Keyboard"

# API キーの設定（安全な方法で設定してください）
api_key = "AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y"  # 環境変数から API キーを取得

# Generative AI モデルの設定
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# ファイルのアップロード
try:
    organ = genai.upload_file("yamamoto/parcussion.jpg")
except Exception as e:
    print(f"Error uploading file: {e}")
    exit(1)

# JSON スキーマの定義
response_schema = {
    "type": "STRING",
    "enum": [choice.value for choice in Choice]
}

# コンテンツの生成
try:
    result = model.generate_content(
        ["What kind of instrument is this:", organ],
        generation_config=genai.GenerationConfig(
            response_mime_type="text/x.enum",
            response_schema=response_schema
        ),
    )
    print(result)
except Exception as e:
    print(f"Error generating content: {e}")

import os

import google.generativeai as genai

genai.configure(api_key='AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y')

print("サポートしているモデル")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


model = genai.GenerativeModel('gemini-pro')

# chat model
chat = model.start_chat(history=[])
while True:
  prompt=input('なにか話してください：　')
  if prompt == 'exit':
    break
  response = chat.send_message(prompt)
  print(response.text)
  
print(chat.history)


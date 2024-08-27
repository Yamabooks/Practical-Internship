import google.generativeai as genai

genai.configure(api_key="AIzaSyBgkZOQx6laXC_DgRBu15CXrXJCNsuM5_Y")
model = genai.GenerativeModel('gemini-pro')

prompt = ("日本で一番高い山は？")

response = model.generate_content(prompt)

assistant_response = response.text

print(f"Assistant: {assistant_response}")
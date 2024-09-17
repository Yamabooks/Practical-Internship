import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening...")
    
    # ノイズ調整
    recognizer.adjust_for_ambient_noise(source)
    
    while True:
        try:
            # マイクからの音声をキャプチャ
            audio = recognizer.listen(source, timeout=5)
            
            # Google Web Speech APIでリアルタイムにテキスト化
            text = recognizer.recognize_google(audio, language="ja-JP")
            print("You said: " + text)
        
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except KeyboardInterrupt:
            print("Stopped")
            break

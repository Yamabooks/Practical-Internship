import copy
import multiprocessing as mp
import soundcard as sc
import json
import numpy as np
import vosk
import sounddevice as sd

def capture_audio_output(audio_queue: mp.Queue,  # 音声認識するプロセスにデータを受け渡すためのキュー
                         capture_sec: float,  # 1回のループで録音する時間
                         sample_rate: int) -> None:  # サンプリング周波数

    num_frame: int = int(sample_rate * capture_sec)

    # デフォルトのマイクを取得
    microphone = sc.default_microphone()

    while True:
        # マイクから音声を録音
        audio = microphone.record(numframes=num_frame, samplerate=sample_rate, blocksize=sample_rate)
        audio_queue.put(copy.copy(audio[:, 0]))  # 音声認識する際はモノラルで良いためaudio[:, 0]としています
        
def speech_to_text(audio_queue: mp.Queue, # 録音するプロセスから音声データを貰うためのキュー
                   sample_rate: int) -> None: # サンプリング周波数
    NO_LOG: int = -1 # VOSK関連のログを出さないためのフラグ
    MODEL_PATH = "C:/Users/chihi/Downloads/vosk-model-ja-0.22/vosk-model-ja-0.22" # モデルのあるディレクトリまでのパス
    
    vosk.SetLogLevel(NO_LOG)
    
    # 以下のようにするとモデル名を指定すると、モデルが/Users/User/.cache/vosk/（パスはWindowsの場合）になければ自動でダウンロードしてくれ、
    # さらに次回以降別のディレクトリでプログラムを実行してもモデルを移動せずにプログラムを実行することができます。
    # model: vosk.Model = vosk.Model(model_name="vosk-model-ja-0.22")
    model: vosk.Model = vosk.Model(model_path=MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, sample_rate)
    
    print("Recognizer is ready")
    print("Output sound from a speaker or a headphone")
    print("#" * 40)
    
    while True:
        audio = audio_queue.get()
        # 音声データを認識に使える形に変換
        audio = map(lambda x: (x+1)/2, audio)
        audio = np.fromiter(audio, np.float16)
        audio = audio.tobytes()
        
        if recognizer.AcceptWaveform(audio): # 音声データの読み込み、話しがちょうどいい区切りの場合、1を返す
            result: json = json.loads(recognizer.Result())
            text = result["text"].replace(" ", "")
            
            if text != "":
                print(text)

def main():
    CAPTURE_SEC: int = 0.4 # 録音するプロセスが1回のループで録音する時間
    
    audio_queue: mp.Queue = mp.Queue() # 録音するプロセスと音声認識するプロセスがやり取りするためのキュー
    sample_rate: int = int(sd.query_devices(kind="output")["default_samplerate"]) # サンプリング周波数は、システムの音声出力の周波数を利用
    stt_proc: mp.Process = mp.Process(target=speech_to_text,
                                      args=(audio_queue, sample_rate)) # 録音するプロセスの作成
    
    print("Type Ctrl+C to stop")
    
    stt_proc.start()
    
    try:
        capture_audio_output(audio_queue=audio_queue, capture_sec=CAPTURE_SEC, sample_rate=sample_rate)
        stt_proc.join()
    except KeyboardInterrupt:
        stt_proc.terminate()
        
        print("/nDone")

if __name__ == '__main__':
    main()
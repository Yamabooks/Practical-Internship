import pyaudio
import wave
from ctypes import CDLL
from pathlib import Path

# DLLの読み込み
CDLL(str(Path("yamamoto/voicevox/onnxruntime_providers_shared.dll").resolve(strict=True)))
CDLL(str(Path("yamamoto/voicevox/onnxruntime.dll").resolve(strict=True)))

from voicevox_core import VoicevoxCore

class VoiceGenerator:
    def __init__(self):
        dictionary_path = "yamamoto/voicevox/open_jtalk_dic_utf_8-1.11"
        self.core = VoicevoxCore(open_jtalk_dict_dir=Path(dictionary_path))
        self.speaker_id = 3
        self.output_file = "yamamoto/codes/voice/output.wav"

        # モデルが読み込まれていない場合はロードする
        if not self.core.is_model_loaded(self.speaker_id):
            self.core.load_model(self.speaker_id)

    def text_to_voice(self, text: str):
        """指定したテキストを音声ファイルに変換する"""
        wave_bytes = self.core.tts(text, self.speaker_id)  # 音声合成を行う
        with open(self.output_file, "wb") as f:
            f.write(wave_bytes)  # ファイルに書き出す
        print(f"音声ファイル '{self.output_file}' が生成されました。")

    def play_wav(self, file_path: str):
        """指定したWAVファイルを再生する"""
        wf = wave.open(file_path, 'rb')
        p = pyaudio.PyAudio()

        # ストリームを開く
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # データをストリームに読み込んで再生
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        # 終了処理
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        print(f"音声ファイル '{file_path}' の再生が完了しました。")
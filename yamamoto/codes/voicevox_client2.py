from ctypes import CDLL
from pathlib import Path

CDLL(str(Path("DLLの場所").resolve(strict=True)))

from voicevox_core import VoicevoxCore

class VoiceGenerator:
    def __init__(self):
        dictionary_path = "open_jtalk_dic_utf_8-1.11"
        self.core = VoicevoxCore(open_jtalk_dict_dir=Path(dictionary_path))
        self.speaker_id = 3
        self.output_file = "out_put.wav"

        # モデルが読み込まれていない場合はロードする
        if not self.core.is_model_loaded(self.speaker_id):
            self.core.load_model(self.speaker_id)

    def text_to_voice(self, text: str):
        """指定したテキストを音声ファイルに変換する"""
        wave_bytes = self.core.tts(text, self.speaker_id)  # 音声合成を行う
        with open(self.output_file, "wb") as f:
            f.write(wave_bytes)  # ファイルに書き出す
        print(f"音声ファイル '{self.output_file}' が生成されました。")
from pathlib import Path
from voicevox_core import VoicevoxCore, METAS

core = VoicevoxCore(open_jtalk_dict_dir=Path("open_jtalk_dic_utf_8-1.11"))

# メタデータ閲覧
#from pprint import pprint
#pprint(METAS)

speaker_id = 38

text = "こんにちは、これはテストです。"
if not core.is_model_loaded(speaker_id):  # モデルが読み込まれていない場合
    core.load_model(speaker_id)  # 指定したidのモデルを読み込む
wave_bytes = core.tts(text, speaker_id)  # 音声合成を行う
with open("output.wav", "wb") as f:
    f.write(wave_bytes)  # ファイルに書き出す

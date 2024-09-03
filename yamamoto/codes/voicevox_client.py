import requests
import json
import pyaudio
import wave
import io
from time import sleep
import subprocess
import psutil
from pydub import AudioSegment

class VoiceVoxClient:
    def __init__(self, speaker_id: int = 3, voicevox_path: str = "C:/Users/chihi/Desktop/VOICEVOX.lnk"):
        self.speaker_id = speaker_id
        self.voicevox_path = voicevox_path
        self.base_url = 'http://localhost:50021'
        self.wav = None
        
        # VOICEVOXが実行中でない場合は起動
        if not self.is_process_running('VOICEVOX.exe'):  # 実際のプロセス名に合わせて変更してください
            self.start_voicevox()
    
    @staticmethod
    def is_process_running(process_name: str) -> bool:
        """指定されたプロセス名が実行中かどうかを確認する。"""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def start_voicevox(self):
        """VOICEVOXアプリケーションを起動する。"""
        subprocess.Popen(['start', self.voicevox_path], shell=True)
    
    def post_audio_query(self, text: str) -> dict:
        """テキストクエリをVOICEVOXに送信し、オーディオクエリのレスポンスを取得する。"""
        params = {'text': text, 'speaker': self.speaker_id}
        res = requests.post(f'{self.base_url}/audio_query', params=params)
        res.raise_for_status()  # エラーレスポンスがあれば例外を発生させる
        return res.json()

    def post_synthesis(self, audio_query_response: dict) -> bytes:
        """オーディオクエリのレスポンスをVOICEVOXに送信し、オーディオデータを取得する。"""
        params = {'speaker': self.speaker_id}
        headers = {'content-type': 'application/json'}
        audio_query_response_json = json.dumps(audio_query_response)
        res = requests.post(
            f'{self.base_url}/synthesis',
            data=audio_query_response_json,
            params=params,
            headers=headers
        )
        res.raise_for_status()  # エラーレスポンスがあれば例外を発生させる
        return res.content

    def text_to_voice(self, text: str):
        """テキストを音声に変換する。"""
        res = self.post_audio_query(text)
        self.wav = self.post_synthesis(res)
        #self.play_wav(wav)
        return self.wav
    
    @staticmethod
    def play_wav(wav_file: bytes):
        """WAVファイルデータをPyAudioで再生する。"""
        wr: wave.Wave_read = wave.open(io.BytesIO(wav_file))
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wr.getsampwidth()),
            channels=wr.getnchannels(),
            rate=wr.getframerate(),
            output=True
        )
        chunk = 1024
        data = wr.readframes(chunk)
        while data:
            stream.write(data)
            data = wr.readframes(chunk)
        sleep(0.5)
        stream.close()
        p.terminate()

    def get_audio_duration(self, audio_data: bytes) -> int:
        """音声データの長さをミリ秒単位で取得する。"""
        #audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
        #return len(audio)
        return 5
        
import requests
import json
import pyaudio
import wave
import io
from time import sleep

import subprocess
import psutil

def is_process_running(process_name):
    # 現在実行中のプロセスを取得
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

# アプリケーション起動
def start_voicevox():
    subprocess.Popen(['start', "C:/Users/chihi/Desktop/VOICEVOX.lnk"], shell=True)

# VOICEVOXのプロセス名を確認して、起動していなければ起動する
if not is_process_running('VOICEVOX.exe'):  # VOICEVOX.exeは実際のプロセス名に合わせて変更してください
    start_voicevox()


def post_audio_query(text: str) -> dict:
    params = {'text': text, 'speaker': 8}
    res = requests.post('http://localhost:50021/audio_query', params=params)
    return res.json()

def post_synthesis(audio_query_response: dict) -> bytes:
    params = {'speaker': 8}
    headers = {'content-type': 'application/json'}
    audio_query_response_json = json.dumps(audio_query_response)
    res = requests.post(
        'http://localhost:50021/synthesis',
        data=audio_query_response_json,
        params=params,
        headers=headers
    )
    return res.content

def play_wav(wav_file: bytes):
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

def text_to_voice(text: str):
    res = post_audio_query(text)
    wav = post_synthesis(res)
    play_wav(wav)

text_to_voice("おはこんばんはろちゃお")
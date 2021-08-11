import os
import sys

import pyaudio
from iterators import TimeoutIterator

from speechkit import DataStreamingRecognition, Session
from speechkit.auth import generate_jwt

CHUNK_SIZE = 4000

service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
key_id = os.environ.get('YANDEX_KEY_ID')
private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()

jwt = generate_jwt(service_account_id, key_id, private_key)
session = Session.from_jwt(jwt)
data_streaming_recognition = DataStreamingRecognition(
    session,
    language_code='ru-RU',
    audio_encoding='LINEAR16_PCM',
    sample_rate_hertz=8000,
    partial_results=False,
    single_utterance=True,
)


def gen_audio_from_file_function():
    with open('/Users/tikhon/Downloads/speech.pcm', 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data != b'':
            yield data
            data = f.read(CHUNK_SIZE)


def gen_audio_capture_function(chunk_size=1024):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=8000,
        input=True,
        frames_per_buffer=chunk_size
    )
    try:
        while True:
            yield stream.read(chunk_size)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


for text, final, end_of_utterance in data_streaming_recognition.recognize(
        gen_audio_capture_function, chunk_size=CHUNK_SIZE
):
    print(text[0])  # text is list of alternatives

    if final:  # Stop when final_flag set
        break

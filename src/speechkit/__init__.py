"""
speechkit
Python SDK for using Yandex Speech recognition and synthesis
"""

__author__ = 'Tikhon Petrishchev'
__version__ = '2.0.0'

from speechkit._auth import Session
from speechkit._recognition.streaming_recognition import DataStreamingRecognition
from speechkit._recognition.sync_recognition import ShortAudioRecognition, RecognitionLongAudio
from speechkit._synthesis import SpeechSynthesis

__all__ = ['Session', 'SpeechSynthesis', 'ShortAudioRecognition', 'RecognitionLongAudio', 'DataStreamingRecognition']

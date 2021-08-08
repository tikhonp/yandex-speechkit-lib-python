import os
import pathlib
import unittest

from speechkit import SpeechSynthesis, Session


class SynthesizeAudio(unittest.TestCase):
    def test_init(self):
        api_key = os.environ.get('SERVICE_API_KEY')
        session = Session.from_api_key(api_key)
        synthesize_audio = SpeechSynthesis(session)
        self.assertIsInstance(synthesize_audio._headers, dict)

    def test_synthesize(self):
        api_key = os.environ.get('SERVICE_API_KEY')
        session = Session.from_api_key(api_key)
        synthesize_audio = SpeechSynthesis(session)

        self.path = os.path.join(os.path.dirname(__file__), 'test_synth.wav')
        synthesize_audio.synthesize(
            self.path, text='text',
            voice='oksana', format='lpcm', sampleRateHertz='16000'
        )
        self.assertTrue(pathlib.Path(self.path).resolve().is_file())

    def test_assert_synthesize(self):
        api_key = os.environ.get('SERVICE_API_KEY')
        session = Session.from_api_key(api_key)
        synthesize_audio = SpeechSynthesis(session)

        with self.assertRaises(ValueError):
            synthesize_audio.synthesize(
                'ok', text='t' * 5001
            )

    def test_synthesize_stream(self):
        api_key = os.environ.get('SERVICE_API_KEY')
        session = Session.from_api_key(api_key)
        synthesize_audio = SpeechSynthesis(session)

        data = synthesize_audio.synthesize_stream(
            text='text', voice='oksana', format='lpcm',
            sampleRateHertz='16000'
        )
        self.assertIsInstance(data, bytes)

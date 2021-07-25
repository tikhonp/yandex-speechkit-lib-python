import unittest
import io
import os

import speechkit


class InvalidDataErrorTestCase(unittest.TestCase):
    def test_raise(self):
        with self.assertRaises(speechkit.InvalidDataError):
            raise speechkit.InvalidDataError()


class RequestErrorTestCase(unittest.TestCase):
    def test_raise_data_1(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'code': 3, 'message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')

    def test_raise_data_2(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'error_code': 3, 'error_message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')


class RecognizeShortAudioTestCase(unittest.TestCase):
    def test_assert_wrong_key_and_wrong_token(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.RecognizeShortAudio('lol')

    def test_init(self):
        api_key = os.environ.get('API_KEY')
        speechkit.RecognizeShortAudio(api_key)

    def test_wrong_catalog(self):
        api_key = os.environ.get('API_KEY')
        recognizeShortAudio = speechkit.RecognizeShortAudio(api_key)

        with self.assertRaises(speechkit.RequestError):
            recognizeShortAudio.recognize(bytes(), folderId='lol')

    def test_recognize(self):
        api_key = os.environ.get('API_KEY')
        recognizeShortAudio = speechkit.RecognizeShortAudio(api_key)

        with open('tests/test.wav', 'rb') as f:
            data = f.read()

        folderId = os.environ.get('CATALOG')
        text = recognizeShortAudio.recognize(
            data, folderId=folderId,
            format='lpcm', sampleRateHertz='48000'
        )
        self.assertIsInstance(text, str)


class ObjectStorageTestCase(unittest.TestCase):
    pass


class RecognizeLongAudio(unittest.TestCase):
    pass


class SynthesizeAudio(unittest.TestCase):
    def test_assert_wrong_key_and_wrong_token(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.SynthesizeAudio('lol')

    def test_init(self):
        api_key = os.environ.get('API_KEY')
        speechkit.SynthesizeAudio(api_key)

    def test_wrong_catalog(self):
        api_key = os.environ.get('API_KEY')
        synthesizeAudio = speechkit.SynthesizeAudio(api_key)

        with self.assertRaises(speechkit.RequestError):
            synthesizeAudio.synthesize_stream(text='text', folderId='lol')


if __name__ == '__main__':
    unittest.main()

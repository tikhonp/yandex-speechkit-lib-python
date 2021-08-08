import os
from unittest import TestCase

from speechkit import Session, DataStreamingRecognition
from speechkit.auth import generate_jwt
import speechkit


class DataStreamingRecognitionTestCase(TestCase):
    def setUp(self) -> None:
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        key_id = os.environ.get('YANDEX_KEY_ID')
        private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()

        jwt = generate_jwt(service_account_id, key_id, private_key)
        self.session = Session.from_jwt(jwt)

    def test_init(self):
        data_streaming_recognition = DataStreamingRecognition(
            self.session,
            language_code='ru-RU',
            audio_encoding='LINEAR16_PCM',
            sample_rate_hertz=8000,
            partial_results=False,
            single_utterance=True,
        )
        self.assertIsInstance(data_streaming_recognition._headers, tuple)

    def test__gen(self):
        def gen_func():
            yield bytes()

        data_streaming_recognition = DataStreamingRecognition(
            self.session,
            language_code='ru-RU',
            audio_encoding='LINEAR16_PCM',
            sample_rate_hertz=8000,
            partial_results=False,
            single_utterance=True,
        )
        next(data_streaming_recognition._gen(gen_func))
        self.assertIsInstance(next(data_streaming_recognition._gen(gen_func)),
                              speechkit._recognition.yandex.cloud.ai.stt.v2.stt_service_pb2.StreamingRecognitionRequest)

    # def test_recognize_raw(self):
    #     self.fail()
    #
    # def test_recognize(self):
    #     self.fail()

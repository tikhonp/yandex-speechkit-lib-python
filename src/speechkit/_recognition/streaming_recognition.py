import logging

import grpc

import speechkit._recognition.yandex.cloud.ai.stt.v2.stt_service_pb2 as stt_service_pb2
import speechkit._recognition.yandex.cloud.ai.stt.v2.stt_service_pb2_grpc as stt_service_pb2_grpc


class DataStreamingRecognition:
    """
    Data streaming mode allows you to simultaneously send audio for recognition and
    get recognition results over the same connection.

    Unlike other recognition methods, you can get intermediate results while speech
    is in progress. After a pause, the service returns final results and starts recognizing the next utterance.

    After receiving the message with the recognition settings, the service starts a recognition session.
    The following limitations apply to each session:

        1. You can't send audio fragments too often or too rarely. The time between messages to the service should be
        approximately the same as the duration of the audio fragments you send, but no more than 5 seconds.
        For example, send 400 ms of audio for recognition every 400 ms.

        2. Maximum duration of transmitted audio for the entire session: 5 minutes.

        3. Maximum size of transmitted audio data: 10 MB.

    To use this type of recognition, you need to create function that yields bytes data

    :Example:

    >>> CHUNK_SIZE = 4000
    >>> session = Session.from_jwt("jwt")
    >>> data_streaming_recognition = DataStreamingRecognition(
    ...     session,
    ...     language_code='ru-RU',
    ...     audio_encoding='LINEAR16_PCM',
    ...     session=8000,
    ...     partial_results=False,
    ...     single_utterance=True,
    ... )
    ...
    >>> def gen_audio_from_file_function():
    ...     with open('/path/to/pcm_data/speech.pcm', 'rb') as f:
    ...         data = f.read(CHUNK_SIZE)
    ...         while data != b'':
    ...             yield data
    ...             data = f.read(CHUNK_SIZE)
    ...
    >>> for i in data_streaming_recognition.recognize(gen_audio_capture_function):
    ...     print(i)  # (['text'], final_flag, end_of_utterance_flag)
    ...

    Read more about streaming recognition in
    `Yandex streaming recognition docs <https://cloud.yandex.com/en/docs/speechkit/stt/streaming>`_
    """

    def __init__(
            self, session, language_code=None, model=None, profanity_filter=None, partial_results=None,
            single_utterance=None, audio_encoding=None, sample_rate_hertz=None, raw_results=None
    ):
        """
        Initialize :py:class:`speechkit.DataStreamingRecognition`

        :param speechkit._auth.Session session: Session instance for auth

        :param string | None language_code: The language to use for recognition. Acceptable values:
            `ru-ru` (case-insensitive, used by default): Russian, `en-us` (case-insensitive): English,
            `tr-tr` (case-insensitive): Turkish.

        :param string | None model: The language model to be used for recognition. The closer the model is matched,
            the better the recognition result. You can only specify one model per request. Default value: `general`.

        :param boolean | None profanity_filter: The profanity filter. Acceptable values:
            `true`: Exclude profanity from recognition results,
            `false` (default): Do not exclude profanity from recognition results.

        :param boolean | None partial_results: The intermediate results filter. Acceptable values:
            `true`: Return intermediate results (part of the recognized utterance).
            For intermediate results, final is set to false,
            `false` (default): Return only the final results (the entire recognized utterance).

        :param boolean | None single_utterance: Flag that disables recognition after the first utterance.
            Acceptable values: `true`: Recognize only the first utterance, stop recognition, and wait for the user
            to disconnect, `false` (default): Continue recognition until the end of the session.

        :param string | None audio_encoding: The format of the submitted audio. Acceptable values:
            `LINEAR16_PCM`: LPCM with no WAV header, `OGG_OPUS` (default): OggOpus format.

        :param integer | None sample_rate_hertz: (int64) The sampling frequency of the submitted audio.
            Required if format is set to LINEAR16_PCM. Acceptable values: `48000` (default): Sampling rate of 48 kHz,
            `16000`: Sampling rate of 16 kHz, `8000`: Sampling rate of 8 kHz.

        :param boolean | None raw_results: Flag that indicates how to write numbers. `true`: In words.
            `false` (default): In figures.
        """
        self._headers = session.streaming_recognition_header
        self._folder_id = session.folder_id

        specification_options = {k: v for k, v in {
            'language_code': language_code, 'model': model, 'profanity_filter': profanity_filter,
            'partial_results': partial_results, 'single_utterance': single_utterance,
            'audio_encoding': audio_encoding, 'sample_rate_hertz': sample_rate_hertz, 'raw_results': raw_results
        }.items() if v is not None}

        config = {'specification': stt_service_pb2.RecognitionSpec(**specification_options)}
        if self._folder_id:
            config['folder_id'] = self._folder_id

        self._streaming_config = stt_service_pb2.RecognitionConfig(**config)

    def _gen(self, gen_audio_function):
        """
        Generate audio fragments.

        :param function gen_audio_function: Function generates audio data
        :return: Serialized data for sending
        """
        try:
            if not callable(gen_audio_function):
                raise RuntimeError("`self._gen_audio_function` must be callable.")

            yield stt_service_pb2.StreamingRecognitionRequest(config=self._streaming_config)

            for data in gen_audio_function():
                yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)

        except Exception as e:
            logging.error(e)
            raise e

    def recognize_raw(self, gen_audio_function):
        """
        Recognize streaming data, gen_audio_function must yield audio data with parameters given in init.
        Answer type read in `Yandex Docs <https://cloud.yandex.com/en/docs/speechkit/stt/streaming#response>`_

        :param function gen_audio_function: Function generates audio data
        :return: Yields recognized data in raw format
        :rtype: speechkit._recognition.yandex.cloud.ai.stt.v2.stt_service_pb2.StreamingRecognitionResponse
        """
        if not callable(gen_audio_function):
            raise RuntimeError("`gen_audio_function` must be callable.")

        cred = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
        stub = stt_service_pb2_grpc.SttServiceStub(channel)

        it = stub.StreamingRecognize(self._gen(gen_audio_function), metadata=(self._headers,))

        for chunk in it:
            yield chunk

    def recognize(self, gen_audio_function):
        """
        Recognize streaming data, gen_audio_function must yield audio data with parameters given in init.

        :param function gen_audio_function: Function generates audio data
        :return: yields tuple, where first element is list of alternatives text, second final (boolean) flag,
            third endOfUtterance (boolean) flag, ex. (['text'], False, False)
        :rtype: tuple
        """
        for item in self.recognize_raw(gen_audio_function):
            alternatives = [i.text for i in item.chunks[0].alternatives]
            final = item.chunks[0].final
            end_of_utterance = item.chunks[0].end_of_utterance
            yield alternatives, final, end_of_utterance

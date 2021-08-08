import requests

from speechkit.exceptions import RequestError


class SpeechSynthesis:
    """Generates speech from received text."""

    def __init__(self, session):
        """
        Initialize :py:class:`speechkit.SpeechSynthesis`

        :param speechkit.Session session: Session instance for auth
        """
        self._headers = session.header
        self._folder_id = session.folder_id

    def _synthesize_stream(self, **kwargs):
        """Creates request to generate speech from text"""

        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        params = {'folderId': self._folder_id} if self._folder_id else {}
        params.update(kwargs)
        answer = requests.post(url, headers=self._headers, data=params, stream=True)

        if not answer.ok:
            raise RequestError(answer.json())

        answer.raw.decode_content = True
        return answer.content

    def synthesize(self, file_path, **kwargs):
        """
        Generates speech from received text and saves it to file

        :type file_path: string
        :param file_path: The path to file where store data

        :type text: string
        :param text: UTF-8 encoded text to be converted to speech.
            You can only use one `text` and `ssml` field.
            For homographs, place a `+` before the stressed vowel.
            For example, `contr+ol` or `def+ect`.
            To indicate a pause between words, use `-`.
            Maximum string length: 5000 characters.

        :type ssml: string
        :param ssml: Text in SSML format to be converted into speech.
            You can only use one text and ssml fields.

        :type lang: string
        :param lang: Language.
            Acceptable values:

            * `ru-RU` (default) — Russian.

            * `en-US` — English.

            * `tr-TR` — Turkish.

        :type voice: string
        :param voice: Preferred speech synthesis voice from the list.
            Default value: `oksana`.

        :type speed: string
        :param speed: Rate (speed) of synthesized speech.
            The rate of speech is set as a decimal number in the range from 0.1 to 3.0. Where:

            * `3.0` — Fastest rate.

            * `1.0` (default) — Average human speech rate.

            * `0.1` — Slowest speech rate.

        :type format: string
        :param format: The format of the synthesized audio. Acceptable values:

            * `lpcm` — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sample_rate_hertz` parameter.

                * Bit depth — 16-bit.

                * Byte order — Reversed (little-endian).

                * Audio data is stored as signed integers.

            * `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using
                the OGG container format (OggOpus).

        :type sampleRateHertz: string
        :param sample_rate_hertz: The sampling frequency of the synthesized audio. Used
            if format is set to lpcm. Acceptable values: * `48000` (default): Sampling rate of 48 kHz. * `16000`:
            Sampling rate of 16 kHz. * `8000`: Sampling rate of 8 kHz.

        :type folderId: string
        :param folderId: ID of the folder that you have access to.
            Required for authorization with a user account (see the UserAccount resource).
            Don't specify this field if you make a request on behalf of a service account.
        """

        if 'text' in kwargs and len(kwargs.get('text', '')) > 5000:
            raise ValueError("Text must be less than 5000 characters")

        with open(file_path, "wb") as f:
            audio_data = self._synthesize_stream(**kwargs)
            f.write(audio_data)

    def synthesize_stream(self, **kwargs):
        """
        Generates speech from received text and return :py:meth:`io.BytesIO` object with data.

        :type text: string
        :param text: UTF-8 encoded text to be converted to speech.
            You can only use one `text` and `ssml` field.
            For homographs, place a `+` before the stressed vowel.
            For example, `contr+ol` or `def+ect`.
            To indicate a pause between words, use `-`.
            Maximum string length: 5000 characters.

        :type ssml: string
        :param ssml: Text in SSML format to be converted into speech.
            You can only use one text and ssml fields.

        :type lang: string
        :param lang: Language.
            Acceptable values:

            * `ru-RU` (default) — Russian.

            * `en-US` — English.

            * `tr-TR` — Turkish.

        :type voice: string
        :param voice: Preferred speech synthesis voice from the list.
            Default value: `oksana`.

        :type speed: string
        :param speed: Rate (speed) of synthesized speech.
            The rate of speech is set as a decimal number in the range from 0.1 to 3.0. Where:

            * `3.0` — Fastest rate.

            * `1.0` (default) — Average human speech rate.

            * `0.1` — Slowest speech rate.

        :type format: string
        :param format: The format of the synthesized audio. Acceptable values:

            - `lpcm` — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sample_rate_hertz` parameter.

                * Bit depth — 16-bit.

                * Byte order — Reversed (little-endian).

                * Audio data is stored as signed integers.

            - `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using
                the OGG container format (OggOpus).

        :type sampleRateHertz: string
        :param sampleRateHertz: The sampling frequency of the synthesized audio.
            Used if format is set to lpcm. Acceptable values:

            * `48000` (default): Sampling rate of 48 kHz.

            * `16000`: Sampling rate of 16 kHz.

            * `8000`: Sampling rate of 8 kHz.

        :type folderId: string
        :param folderId: ID of the folder that you have access to.
            Required for authorization with a user account (see the UserAccount resource).
            Don't specify this field if you make a request on behalf of a service account.
        """
        if 'text' in kwargs and len(kwargs.get('text', '')) > 5000:
            raise ValueError("Text must be less than 5000 characters")

        return self._synthesize_stream(**kwargs)
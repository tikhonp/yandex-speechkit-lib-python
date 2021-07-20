"""speechkit
Python SDK for using Yandex Speech recognition and synthesis
"""

import requests
import boto3

__author__ = 'Tikhon Petrishchev'
__version__ = '1.3.1'


class RecognizeShortAudio:
    """
    Short audio recognition ensures fast response time and is suitable for single-channel audio of small length.

    Audio requirements:
        * Maximum file size: 1 MB.
        * Maximum length: 30 seconds.
        * Maximum number of audio channels: 1.

    """
    # TODO: Add checking with this parametrs

    def __init__(self, yandex_passport_oauth_token):
        """Gets IAM token and stores in `RecognizeShortAudio.token`

        :type yandex_passport_oauth_token: string
        :param yandex_passport_oauth_token: OAuth token from Yandex.OAuth
        """

        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": yandex_passport_oauth_token}
        answer = requests.post(url, json=data).json()

        try:
            self.token = answer['iamToken']
        except KeyError:
            raise ValueError("Invalid 'yandex_passport_oauth_token', "
                             "oringinal exception: '{}'".format(answer))

    def recognize(self, data, **kwargs):
        """
        Recognize text from BytesIO data given, which is audio

        :type data: io.BytesIO
        :param data: Data with audio samples to recognize

        :type lang: string
        :param lang: The language to use for recognition. Acceptable values:
            * `ru-RU` (by default) — Russian.
            * `en-US` — English.
            * `tr-TR` — Turkish.

        :type topic: string
        :param topic: The language model to be used for recognition. Default value: `general`.

        :type profanityFilter: boolean
        :param profanityFilter: This parameter controls the profanity filter in recognized speech.

        :type format: string
        :param format: The format of the submitted audio. Acceptable values:
            * `lpcm` — LPCM with no WAV header.
            * `oggopus` (default) — OggOpus.

        :type sampleRateHertz: string
        :param sampleRateHertz: The sampling frequency of the submitted audio.
            Used if format is set to lpcm. Acceptable values:
            * `48000` (default) — Sampling rate of 48 kHz.
            * `16000` — Sampling rate of 16 kHz.
            * `8000` — Sampling rate of 8 kHz.

        :type folderId: string
        :param folderId: ID of the folder that you have access to. Don't specify this field if you make a request on behalf of a service account.

        :return: The recognized text, string
        """

        url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
        headers = {'Authorization': 'Bearer {}'.format(self.token)}

        answer = requests.post(url, params=kwargs, data=data, headers=headers)

        if answer.status_code != 200:
            raise Exception(
                "It's error when recognizing: '{}'".format(answer.json()))
        else:
            return answer.json()['result']


class ObjectStorage:
    """Interact with AWS object storage.

    :type aws_access_key_id: string
    :param aws_access_key_id: The access key to use when creating the client.  This is entirely optional, and if not provided, the credentials configured for the session will automatically be used.  You only need to provide this argument if you want to override the credentials used for this specific client.

    :type aws_secret_access_key: string
    :param aws_secret_access_key: The secret key to use when creating the client.  Same semantics as aws_access_key_id above.

    :type aws_session_token: string
    :param aws_session_token: The session token to use when creating the client.  Same semantics as aws_access_key_id above.
    """

    def __init__(self, **kwargs):
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            **kwargs
        )

    def upload_file(self, file_path, baketname, aws_file_name):
        """Upload a file to object storage

        :type file_path: string
        :param file_path: Path to input file
        :type baketname: string
        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage
        """
        return self.s3.upload_file(file_path, baketname, aws_file_name)

    def list_objects_in_bucket(self, bucketname):
        """Get list of all objects in backet"""

        return self.s3.list_objects(Bucket=bucketname)

    def delete_object(self, aws_file_name, bucketname):
        """Delete object in bucket

        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage
        :type bucketname: string
        """

        return self.s3.delete_objects(
            Bucket=bucketname, Delete={'Objects': [{'Key': aws_file_name}]})

    def create_presigned_url(self, bucket_name, aws_file_name,
                             expiration=3600):
        """Generate a presigned URL to share an S3 object

        :type bucket_name: string

        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage

        :type expiration: integer
        :param expiration: Time in seconds for the presigned URL to remain valid

        :return: Presigned URL as string.
        """

        return self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': aws_file_name},
            ExpiresIn=expiration
        )


class RecognizeLongAudio:
    """
    Long audio fragment recognition can be used
        for multi-channel audio files up to 1 GB.

    To recognize long audio fragments, you need to execute 2 requests:
        * Send a file for recognition.
        * Get recognition results.

        >>> recognizeLongAudio = RecognizeLongAudio('<Api-Key>')
        >>> recognizeLongAudio.send_for_recognition('<object storage uri>')
        >>> if recognizeLongAudio.get_recognition_results():
        ...     data = recognizeLongAudio.get_data()
        ...
        >>> recognizeLongAudio.get_raw_text()
        'raw recognized text'
    """

    def __init__(self, api_key):
        """Initialize Api-Key for recognizing long audio

        :type api_key: string
        :param api_key: The API key is a private key used for simplified
            authorization in the Yandex.Cloud API.
        """

        self.api_key = api_key
        self.header = {'Authorization': 'Api-Key {}'.format(self.api_key)}

    def send_for_recognition(self, uri, **kwargs):
        """Send a file for recognition

        :type uri: string
        :param uri: The URI of the audio file for recognition.
            Supports only links to files stored in Yandex Object Storage.

        :type languageCode: string
        :param languageCode: The language that recognition will be performed for.
            Only Russian is currently supported (`ru-RU`).

        :type model: string
        :param model: The language model to be used for recognition.
            Default value: `general`.

        :type profanityFilter: boolean
        :param profanityFilter: The profanity filter.

        :type audioEncoding: string
        :param audioEncoding: The format of the submitted audio.
            Acceptable values:

            * `LINEAR16_PCM`: LPCM with no WAV header.

            * `OGG_OPUS` (default): OggOpus format.

        :type sampleRateHertz: integer
        :param sampleRateHertz: The sampling frequency of the submitted audio.
            Required if format is set to LINEAR16_PCM. Acceptable values:
            * `48000` (default): Sampling rate of 48 kHz.
            * `16000`: Sampling rate of 16 kHz.
            * `8000`: Sampling rate of 8 kHz.

        :type audioChannelCount: integer
        :param audioChannelCount: The number of channels in LPCM files.
            By default, `1`. Don't use this field for OggOpus files.

        :type rawResults: boolean
        :param rawResults: Flag that indicates how to write numbers.
            `true`: In words. `false` (default): In figures.
        """

        url = "https://transcribe.api.cloud.yandex.net/" \
            "speech/stt/v2/longRunningRecognize"
        data = {
            "config": {
                "specification": {
                    **kwargs
                }
            },
            "audio": {
                "uri": uri
            }
        }
        answer = requests.post(url, headers=self.header, json=data).json()
        self.id = answer['id']

    def get_recognition_results(self):
        """Monitor the recognition results using the received ID.
        The number of result monitoring requests is limited,
        so consider the recognition speed: it takes about 10 seconds
        to recognize 1 minute of single-channel audio.
        """

        url = "https://operation.api.cloud.yandex.net/operations/{id}"
        self.answer = requests.get(
            url.format(id=self.id), headers=self.header).json()
        return self.answer['done']

    def get_data(self):
        """Get the response.
        Use :meth:`RecognizeLongAudio.get_recognition_results` first to store answer

        Contain a list of recognition results (`chunks[]`).

        :return: Each result in the chunks[] list contains the following fields:

            * `alternatives[]`: List of recognized text alternatives. Each alternative contains the following fields:

                * `words[]`: List of recognized words:

                    * `startTime`: Time stamp of the beginning of the word in the recording. An error of 1-2 seconds is possible.

                    * `endTime`: Time stamp of the end of the word. An error of 1-2 seconds is possible.

                    * `word`: Recognized word. Recognized numbers are written in words (for example, twelve rather than 12).

                    * `confidence`: This field currently isn't supported. Don't use it.

                    * `text`: Full recognized text. By default, numbers are written in figures. To output the entire text in words, specify true in the raw_results field.

                    * `confidence`: This field currently isn't supported. Don't use it.

            * `channelTag`: Audio channel that recognition was performed for.
        """
        if not hasattr(self, 'answer'):
            raise ValueError("You must call 'get_recognition_results' first")
        return self.answer['results']

    def get_raw_text(self):
        """Get raw text from answer data

        :return: Text
        """

        text = ''
        for chunk in self.answer['response']['chunks']:
            text += chunk['alternatives'][0]['text']
        return text


class SynthesizeAudio:
    """Generates speech from received text."""

    def __init__(self, yandex_passport_oauth_token):
        """
        :type yandex_passport_oauth_token: string
        :param yandex_passport_oauth_token: OAuth token from Yandex.OAuth
        """

        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": yandex_passport_oauth_token}
        answer = requests.post(url, json=data).json()

        try:
            self.token = answer['iamToken']
        except KeyError:
            raise ValueError("Invalid 'yandex_passport_oauth_token', "
                             "oringinal exception: '{}'".format(answer))

    def _synthesize_stream(self, **kwargs):
        """Creates request to generate speech from text"""

        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {
            'Authorization': 'Bearer ' + self.token,
        }

        answer = requests.post(url, headers=headers, data=kwargs, stream=True)
        if answer.status_code != 200:
            raise RuntimeError(
                "Invalid response received: code: %d, message: %s" % (
                    answer.status_code, answer.text))
        answer.raw.decode_content = True
        return answer.content

    def synthesize(self, file_path, **kwargs):
        """Generates speech from received text and saves it to file

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
            * `lpcm` — Audio file is synthesized in LPCM format with no WAV header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sampleRateHertz` parameter.
                * Bit depth — 16-bit.
                * Byte order — Reversed (little-endian).
                * Audio data is stored as signed integers.

            * `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using the OGG container format (OggOpus).

        :type sampleRateHertz: string
        :param sampleRateHertz: The sampling frequency of the synthesized audio. Used if format is set to lpcm. Acceptable values:
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

        with open(file_path, "wb") as f:
            audio_data = self._synthesize_stream(**kwargs)
            f.write(audio_data)

    def synthesize_stream(self, **kwargs):
        """Generates speech from received text and return `io.BytesIO` object
            with data.

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
            * `lpcm` — Audio file is synthesized in LPCM format with no WAV header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sampleRateHertz` parameter.
                * Bit depth — 16-bit.
                * Byte order — Reversed (little-endian).
                * Audio data is stored as signed integers.

            * `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using the OGG container format (OggOpus).

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

        return self._synthesize_stream(**kwargs)

"""speechkit
Python SDK for using Yandex Speech recognition and synthesis
"""

__author__ = 'Tikhon Petrishchev'
__version__ = '1.4.0'

import io
import sys
import uuid
from pathlib import Path
from typing import List

import boto3
import requests


class InvalidDataError(ValueError):
    """Exception raised for errors when data not valid"""
    pass


class RequestError(Exception):
    """Exception raised for errors while yandex api request"""

    def __init__(self, answer: dict, *args):
        self.error_code = str(answer.get('code', '')) + str(answer.get('error_code', ''))
        self.message = str(answer.get('message', '')) + str(answer.get('error_message', ''))
        super().__init__(self.error_code + ' ' + self.message, *args)


def get_iam_token(yandex_passport_oauth_token: str = None, jwt: str = None) -> str:
    """Creates an IAM token for the specified identity."""

    if (not yandex_passport_oauth_token and not jwt) or (yandex_passport_oauth_token and jwt):
        raise InvalidDataError("Includes only one of the fields `yandexPassportOauthToken`, `jwt`")

    if yandex_passport_oauth_token:
        data = {'yandexPassportOauthToken': str(yandex_passport_oauth_token)}
    else:
        data = {'jwt': str(jwt)}

    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    answer = requests.post(url, json=data)

    if answer.ok:
        return answer.json().get('iamToken')
    else:
        raise RequestError(answer.json())


def get_api_key(yandex_passport_oauth_token: str = None, service_account_id: str = None,
                description: str = 'Default Api-Key created by `speechkit` python SDK') -> str:
    """Creates an API key for the specified service account."""

    if not yandex_passport_oauth_token or not service_account_id:
        raise InvalidDataError("`yandex_passport_oauth_token` and `service_account_id` required.")

    url = 'https://iam.api.cloud.yandex.net/iam/v1/apiKeys'
    headers = {
        'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
    }
    data = {'serviceAccountId': service_account_id, 'description': description}

    answer = requests.post(url, headers=headers, json=data)
    if answer.ok:
        return answer.json().get('secret')
    else:
        raise RequestError(answer.json())


def list_of_service_accounts(yandex_passport_oauth_token, folder_id, **kwargs) -> List[dict]:
    """Retrieves the list of ServiceAccount resources in the specified folder."""

    headers = {
        'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
    }
    url = 'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts'
    data = {'folderId': folder_id, **kwargs}
    answer = requests.get(url, headers=headers, json=data)
    if answer.ok:
        return answer.json().get('serviceAccounts', [])
    else:
        raise RequestError(answer.json())


class RecognizeShortAudio:
    """
    Short audio recognition ensures fast response time and is suitable for single-channel audio of small length.

    Audio requirements:
        * Maximum file size: 1 MB.
        * Maximum length: 30 seconds.
        * Maximum number of audio channels: 1.

    """

    def __init__(self, yandex_passport_oauth_token):
        """Gets IAM _token and stores in `RecognizeShortAudio._token`

        :type yandex_passport_oauth_token: string
        :param yandex_passport_oauth_token: OAuth _token from Yandex.OAuth
        :return: __init__ should return None
        :rtype: None
        """

        if not type(yandex_passport_oauth_token) is str:
            raise TypeError("__init__() yandex_passport_oauth_token: got {} but expected \
                            type is str".format(type(yandex_passport_oauth_token).__name__))

        self._headers = {
            'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
        }

    def recognize(self, data, **kwargs):
        """
        Recognize text from BytesIO data given, which is audio

        :type data: io.BytesIO, bytes
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

            * `lpcm` — LPCM with no WAV _header.

            * `oggopus` (default) — OggOpus.

        :type sampleRateHertz: string
        :param sampleRateHertz: The sampling frequency of the submitted audio.
            Used if format is set to lpcm. Acceptable values:

            * `48000` (default) — Sampling rate of 48 kHz.

            * `16000` — Sampling rate of 16 kHz.

            * `8000` — Sampling rate of 8 kHz.

        :type folderId: string :param folderId: ID of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.

        :return: The recognized text
        :rtype: string
        """

        if not isinstance(data, (io.BytesIO, bytes)):
            raise InvalidDataError("Data must be bytes io or bytes.")

        if 'lang' in kwargs:
            if not type(kwargs['lang']) is str:
                raise TypeError("__init__() kwargs['lang']: got {} but expected \
                type is str".format(type(kwargs["lang"]).__name__))

        if self._headers is None:
            raise RuntimeError("You must call `RecognizeShortAudio.__init__()` first.")

        if sys.getsizeof(data) > 1024 * 1024:
            raise InvalidDataError("Maximum file size: 1 MB. Got {} bytes.".format(sys.getsizeof(data)))

        if kwargs.get('format') == 'lpcm':
            sample_rate_hertz = int(kwargs.get('sampleRateHertz', '48000'))
            seconds_duration = (sys.getsizeof(data) * 8) / (sample_rate_hertz * 1 * 16)

            if seconds_duration > 30:
                raise InvalidDataError(
                    "Maximum length: 30 seconds. Maximum number of audio channels: 1. Calculated length - {}".format(
                        seconds_duration))

        url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
        answer = requests.post(url, params=kwargs, data=data, headers=self._headers)

        if answer.ok:
            return answer.json().get('result')
        else:
            raise RequestError(answer.json())


class RecognizeLongAudio:
    """
    Long audio fragment recognition can be used
        for multi-channel audio files up to 1 GB.

    To recognize long audio fragments, you need to execute 2 requests:
        * Send a file for recognition.
        * Get recognition results.

        >>> recognizeLongAudio = RecognizeLongAudio('<yandex_passport_oauth_token>', '<service_account_id>')
        >>> recognizeLongAudio.send_for_recognition('file/path')
        >>> if recognizeLongAudio.get_recognition_results():
        ...     data = recognizeLongAudio.get_data()
        ...
        >>> recognizeLongAudio.get_raw_text()
        'raw recognized text'
    """

    def __init__(self, yandex_passport_oauth_token, service_account_id, aws_bucket_name=None,
                 aws_credentials_description='Default AWS credentials created by `speechkit` python SDK',
                 aws_region_name='ru-central1'):
        """Initialize Api-Key for recognizing long audio

        :type api_key: string
        :param api_key: The API key is a private key used for simplified
            authorization in the Yandex.Cloud API.

        :return: __init__ should return None
        :rtype: None
        """
        self._id = None
        self._answer_data = None
        self._aws_file_name = None

        if not isinstance(yandex_passport_oauth_token, str) or yandex_passport_oauth_token == '':
            raise InvalidDataError("`yandex_passport_oauth_token` must be not empty string, but got `{}`".format(
                yandex_passport_oauth_token))

        if len(aws_credentials_description) > 256:
            raise InvalidDataError("The maximum `description` string length in characters is 256.")

        self._headers = {
            'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
        }

        url_aws_credentials = 'https://iam.api.cloud.yandex.net/iam/aws-compatibility/v1/accessKeys'
        data_aws_credentials = {'description': aws_credentials_description, 'serviceAccountId': service_account_id}
        answer = requests.post(url_aws_credentials, headers=self._headers, json=data_aws_credentials)

        if not answer.ok:
            raise RequestError(answer.json())

        answer = answer.json()
        self._s3 = self._init_aws(
            aws_access_key_id=answer.get('accessKey', {}).get('keyId'),
            aws_secret_access_key=answer.get('secret'),
            region_name=aws_region_name,
        )

        if aws_bucket_name:
            self._aws_bucket_name = aws_bucket_name
        else:
            self._aws_bucket_name = 'py_speechkit_' + str(uuid.uuid4())
            self._s3.create_bucket(Bucket=self._aws_bucket_name)

        self._api_key_headers = {
            'Authorization': 'Api-Key {}'.format(get_api_key(
                yandex_passport_oauth_token, service_account_id
            ))
        }

    @staticmethod
    def _init_aws(**kwargs):
        """Get s3 session

        :param string aws_access_key_id: The access key to use when creating the client.  This is entirely optional,
        and if not provided, the credentials configured for the session will automatically be used. You only need to
        provide this argument if you want to override the credentials used for this specific client.

        :param  string aws_secret_access_key: The secret key to use when creating the client. Same semantics as
        aws_access_key_id above.

        :param string region_name: The name of the region associated with the client.
            A client is associated with a single region.
        """

        session = boto3.session.Session()
        return session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            **kwargs
        )

    def _aws_upload_file(self, file_path, baket_name, aws_file_name):
        """Upload a file to object storage

        :type file_path: string
        :param file_path: Path to input file
        :type baket_name: string
        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage
        """
        return self._s3.upload_file(file_path, baket_name, aws_file_name)

    def _create_presigned_url(self, bucket_name, aws_file_name,
                              expiration=3600):
        """Generate a presigned URL to share an S3 object

        :type bucket_name: string

        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage

        :type expiration: integer
        :param expiration: Time in seconds for the presigned URL to remain valid

        :return: Resigned URL as string.
        """

        return self._s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': aws_file_name},
            ExpiresIn=expiration
        )

    def _delete_object(self, bucket_name, aws_file_name):
        """Delete object in bucket

        :type aws_file_name: string
        :param aws_file_name: Name of file in object storage
        :type bucket_name: string
        """

        return self._s3.delete_objects(
            Bucket=bucket_name, Delete={'Objects': [{'Key': aws_file_name}]})

    def send_for_recognition(self, file_path, **kwargs):
        """Send a file for recognition

        :type file_path: string
        :param file_path: Path to input file

        :param string folder_id: ID of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.

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

            * `LINEAR16_PCM`: LPCM with no WAV _header.

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

        self._aws_file_name = Path(file_path).name + str(uuid.uuid4())
        self._aws_upload_file(file_path, self._aws_bucket_name, self._aws_file_name)
        aws_presigned_url = self._create_presigned_url(self._aws_bucket_name, self._aws_file_name)

        url = "https://transcribe.api.cloud.yandex.net/" \
              "speech/stt/v2/longRunningRecognize"
        data = {

            "config": {
                "specification": {
                    **kwargs
                }
            },
            "audio": {
                "uri": aws_presigned_url
            }
        }
        answer = requests.post(url, headers=self._api_key_headers, json=data)
        if answer.ok:
            self._id = answer.json().get('id')
        else:
            raise RequestError(answer.json())

    def get_recognition_results(self) -> bool:
        """Monitor the recognition results using the received ID.
        The number of result monitoring requests is limited,
        so consider the recognition speed: it takes about 10 seconds
        to recognize 1 minute of single-channel audio.
        """

        if self._id is None:
            raise RuntimeError("You must send for recognition first.")

        url = "https://operation.api.cloud.yandex.net/operations/{id}".format(id=self._id)
        self._answer_data = requests.get(url, headers=self._headers)
        if self._answer_data.ok:
            self._answer_data = self._answer_data.json()
            done = self._answer_data.get('done')
            if done:
                self._delete_object(self._aws_bucket_name, self._aws_file_name)

            return done
        else:
            raise RequestError(self._answer_data.json())

    def get_data(self):
        """Get the response.
        Use :meth:`RecognizeLongAudio.get_recognition_results` first to store _answer_data

        Contain a list of recognition results (`chunks[]`).

        :return: `None` if text not found ot Each result in the chunks[] list contains the following fields:

            * `alternatives[]`: List of recognized text alternatives. Each alternative contains the following fields:

                * `words[]`: List of recognized words:

                    * `startTime`: Time stamp of the beginning of the word in the recording. An error of 1-2 seconds
                        is possible.

                    * `endTime`: Time stamp of the end of the word. An error of 1-2 seconds is possible.

                    * `word`: Recognized word. Recognized numbers are written in words (for example, twelve rather
                        than 12).

                    * `confidence`: This field currently isn't supported. Don't use it.

                    * `text`: Full recognized text. By default, numbers are written in figures. To output the entire
                        text in words, specify true in the raw_results field.

                    * `confidence`: This field currently isn't supported. Don't use it.

            * `channelTag`: Audio channel that recognition was performed for.

        """

        if self._answer_data is None:
            raise ValueError("You must call `RecognizeLongAudio.get_recognition_results` first")
        return self._answer_data.get('results')

    def get_raw_text(self):
        """Get raw text from _answer_data data

        :return: Text
        """

        if self._answer_data is None:
            raise ValueError("You must call 'get_recognition_results' first")

        text = ''
        for chunk in self._answer_data.get('response', {}).get('chunks', []):
            text += chunk['alternatives'][0]['text']
        return text


class SynthesizeAudio:
    """Generates speech from received text."""

    def __init__(self, yandex_passport_oauth_token):
        """
        :type yandex_passport_oauth_token: string
        :param yandex_passport_oauth_token: OAuth _token from Yandex.OAuth
        """

        self._headers = {
            'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
        }

    def _synthesize_stream(self, **kwargs):
        """Creates request to generate speech from text"""

        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        answer = requests.post(url, headers=self._headers, data=kwargs, stream=True)

        if not answer.ok:
            raise RequestError(answer.json())

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
            * `lpcm` — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sampleRateHertz` parameter.

                * Bit depth — 16-bit.

                * Byte order — Reversed (little-endian).

                * Audio data is stored as signed integers.

            * `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using
                the OGG container format (OggOpus).

        :type sampleRateHertz: string :param sampleRateHertz: The sampling frequency of the synthesized audio. Used
            if format is set to lpcm. Acceptable values: * `48000` (default): Sampling rate of 48 kHz. * `16000`:
            Sampling rate of 16 kHz. * `8000`: Sampling rate of 8 kHz.

        :type folderId: string
        :param folderId: ID of the folder that you have access to.
            Required for authorization with a user account (see the UserAccount resource).
            Don't specify this field if you make a request on behalf of a service account.
        """

        if 'text' in kwargs and len(kwargs.get('text', '')) > 5000:
            raise InvalidDataError("Text must be less than 5000 characters")

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
            * `lpcm` — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

                * Sampling — 8, 16, or 48 kHz, depending on the value of the `sampleRateHertz` parameter.

                * Bit depth — 16-bit.

                * Byte order — Reversed (little-endian).

                * Audio data is stored as signed integers.

            * `oggopus` (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using
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
            raise InvalidDataError("Text must be less than 5000 characters")

        return self._synthesize_stream(**kwargs)

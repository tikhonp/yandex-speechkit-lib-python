import io
import sys
import uuid
from pathlib import Path

import boto3
import requests

from speechkit.exceptions import RequestError


class ShortAudioRecognition:
    """
    Short audio recognition ensures fast response time and is suitable for single-channel audio of small length.

    Audio requirements:
        1. Maximum file size: 1 MB.
        2. Maximum length: 30 seconds.
        3. Maximum number of audio channels: 1.

    If your file is larger, longer, or has more audio channels, use :py:class:`speechkit.RecognitionLongAudio`.
    """

    def __init__(self, session):
        """
        Initialization :py:class:`speechkit.ShortAudioRecognition`

        :param speechkit.Session session: Session instance for auth
        """
        self._headers = session.header
        self._folder_id = session.folder_id

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

        :param string sampleRateHertz: The sampling frequency of the submitted audio.
            Used if format is set to lpcm. Acceptable values:

            * `48000` (default) — Sampling rate of 48 kHz.

            * `16000` — Sampling rate of 16 kHz.

            * `8000` — Sampling rate of 8 kHz.

        :param string folderId: ID of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.

        :return: The recognized text
        :rtype: string
        """
        if not isinstance(data, (io.BytesIO, bytes)):
            raise ValueError("Data must be bytes io or bytes.")

        if 'lang' in kwargs:
            if not type(kwargs['lang']) is str:
                raise TypeError("__init__() kwargs['lang']: got {} but expected \
                type is str".format(type(kwargs["lang"]).__name__))

        if self._headers is None:
            raise RuntimeError("You must call `ShortAudioRecognition.__init__()` first.")

        if sys.getsizeof(data) > 1024 * 1024:
            raise ValueError("Maximum file size: 1 MB. Got {} bytes.".format(sys.getsizeof(data)))

        if kwargs.get('format') == 'lpcm':
            sample_rate_hertz = int(kwargs.get('sample_rate_hertz', '48000'))
            seconds_duration = (sys.getsizeof(data) * 8) / (sample_rate_hertz * 1 * 16)

            if seconds_duration > 30:
                raise ValueError(
                    "Maximum length: 30 seconds. Maximum number of audio channels: 1. Calculated length - {}".format(
                        seconds_duration))

        params = {'folderId': self._folder_id} if self._folder_id else {}
        params.update(kwargs)
        url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
        answer = requests.post(url, params=params, data=data, headers=self._headers)

        if answer.ok:
            return answer.json().get('result')
        else:
            raise RequestError(answer.json())


class RecognitionLongAudio:
    """
    Long audio fragment recognition can be used for multi-channel audio files up to 1 GB.
    To recognize long audio fragments, you need to execute 2 requests:

        * Send a file for recognition.

        * Get recognition results.

    :Example:

    >>> recognizeLongAudio = RecognitionLongAudio(session, '<service_account_id>')
    >>> recognizeLongAudio.send_for_recognition('file/path')
    >>> if recognizeLongAudio.get_recognition_results():
    ...     data = recognizeLongAudio.get_data()
    ...
    >>> recognizeLongAudio.get_raw_text()
    ...'raw recognized text'
    """

    def __init__(self, session, service_account_id, aws_bucket_name=None,
                 aws_credentials_description='Default AWS credentials created by `speechkit` python SDK',
                 aws_region_name='ru-central1'):
        """
        Initialize :py:class:`speechkit.RecognitionLongAudio`

        :param speechkit.Session session: Session instance for auth
        """
        self._id = None
        self._answer_data = None
        self._aws_file_name = None

        if len(aws_credentials_description) > 256:
            raise ValueError("The maximum `description` string length in characters is 256.")

        self._headers = session.header
        if session.folder_id:
            raise ValueError("folder_id specify is not supported, use jwt.")
        if session.auth_method == session.API_KEY:
            raise ValueError("Only jwt method supported")

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
        :rtype: string
        """

        return self._s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': aws_file_name},
            ExpiresIn=expiration
        )

    def _delete_object(self, bucket_name, aws_file_name):
        """Delete object in bucket

        :param string aws_file_name: Name of file in object storage
        :type bucket_name: string
        """
        return self._s3.delete_objects(
            Bucket=bucket_name, Delete={'Objects': [{'Key': aws_file_name}]})

    def send_for_recognition(self, file_path, **kwargs):
        """
        Send a file for recognition

        :param string file_path: Path to input file

        :param string folder_id: ID of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.

        :param string languageCode: The language that recognition will be performed for.
            Only Russian is currently supported (`ru-RU`).

        :param string model: The language model to be used for recognition.
            Default value: `general`.

        :param boolean profanityFilter: The profanity filter.

        :param string audioEncoding: The format of the submitted audio.
            Acceptable values:

            * `LINEAR16_PCM`: LPCM with no WAV _header.

            * `OGG_OPUS` (default): OggOpus format.

        :param integer sampleRateHertz: The sampling frequency of the submitted audio.
            Required if format is set to LINEAR16_PCM. Acceptable values:

            * `48000` (default): Sampling rate of 48 kHz.

            * `16000`: Sampling rate of 16 kHz.

            * `8000`: Sampling rate of 8 kHz.

        :param integer audioChannelCount: The number of channels in LPCM files.
            By default, `1`. Don't use this field for OggOpus files.

        :param boolean rawResults: Flag that indicates how to write numbers.
            `true`: In words. `false` (default): In figures.

        :rtype: None
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
        answer = requests.post(url, headers=self._headers, json=data)
        if answer.ok:
            self._id = answer.json().get('id')
        else:
            raise RequestError(answer.json())

    def get_recognition_results(self):
        """
        Monitor the recognition results using the received ID. The number of result monitoring requests is limited,
        so consider the recognition speed: it takes about 10 seconds to recognize 1 minute of single-channel audio.

        :return: State of recognition is done or not
        :rtype: boolean
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
        """
        Get the response.
        Use :py:meth:`speechkit.RecognitionLongAudio.get_recognition_results` first to store _answer_data

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

                    * `text`: Full recognized text. By default, numbers are written in figures. To recognition
                        the entire text in words, specify true in the raw_results field.

                    * `confidence`: This field currently isn't supported. Don't use it.

            * `channelTag`: Audio channel that recognition was performed for.
        :rtype: list | None
        """

        if self._answer_data is None:
            raise ValueError("You must call `RecognitionLongAudio.get_recognition_results` first")
        return self._answer_data.get('results')

    def get_raw_text(self):
        """
        Get raw text from _answer_data data

        :return: Text
        :rtype: string
        """
        if self._answer_data is None:
            raise ValueError("You must call 'get_recognition_results' first")

        text = ''
        for chunk in self._answer_data.get('response', {}).get('chunks', []):
            text += chunk['alternatives'][0]['text']
        return text

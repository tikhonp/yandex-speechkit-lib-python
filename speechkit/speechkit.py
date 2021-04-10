import requests
from io import BytesIO
from os import system


class RecognizeShortAudio:
    def __init__(self, key):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": key}
        answer = requests.post(url, json=data)

        # print(answer.json()['iamToken'])
        self.token = answer.json()['iamToken']

    def recognize(self, file, folder):
        """
        Recognizes audio file
        :param file: string, path to audio file OOGopus format
            (You can use recode function to get oogopus)
        :param folder: string, yandex catalog id, instruction:
            https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id
        """
        url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
        headers = {"Authorization": "Bearer {}".format(self.token)}
        params = {
            'lang': 'ru-RU',
            'folderId': folder,
            'format': 'lpcm',
            'sampleRateHertz': 48000,
        }

        answer = requests.post(url, params=params, data=file, headers=headers)

        if answer.status_code != 200:
            raise Exception(
                "It's error with recognizing: {}".format(answer.json()))
        else:
            return answer.json()['result']


def recode(inputfile: str, outputfile: str):
    """Recodering file using ffmpeg

    :param inputfile: string, path to input file
    :param outputfile: string, path to output file
    """

    cmd = "ffmpeg -i '" + str(inputfile) + "' '" + str(outputfile) + "'"
    out = system(cmd)
    return out


def removefile(inputfile: str):
    """Removes file

    :param inputfile: string, path to input file
    """

    cmd = "rm '" + str(inputfile) + "'"
    out = system(cmd)
    return out


class ObjectStorage:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        """Starting ssesion with boto3 to access objectStorage

        :param aws_access_key_id: string
        :param aws_secret_access_key: string
        """

        import boto3
        # system("cd ~")
        # system("mkdir .aws")
        # system("echo '[default] \nregion=ru-central1' > .aws/config")
        # system("echo '[default] \naws_access_key_id = {} \naws_secret_access_key = {}' > .aws/credentials".format(aws_access_key_id, aws_secret_access_key))
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def upload_file(self, inputfilepath, baketname, outputfilename):
        """Upload a file to object storage

        :param inputfilepath: string, path to input file
        :param baketname: string
        :param outputfilename: string, name of file in object storage
        """

        return self.s3.upload_file(inputfilepath, baketname, outputfilename)

    def listObjectsInBucket(self, bucketname):
        return self.s3.list_objects(Bucket=bucketname)

    def deleteObject(self, object_name, bucketname):
        return self.s3.delete_objects(
            Bucket=bucketname, Delete={'Objects': [{'Key': object_name}]})

    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds
            for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
        except Exception as e:
            print(e)
            return None

        # The response contains the presigned URL
        return response


class RecognizeLongAudio:
    def __init__(self, apiKey):
        """Initialize apiKey for recognizing long audio

        :param apiKey: string
        """

        self.apiKey = apiKey
        self.header = {'Authorization': 'Api-Key {}'.format(self.apiKey)}

    def recognize_post(self, filelink):
        """POST request to recognize long audio

        :param filelink: string
        """

        POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
        body = {
            "config": {
                "specification": {
                    "languageCode": "ru-RU"
                }
            },
            "audio": {
                "uri": filelink
            }
        }
        req = requests.post(POST, headers=self.header, json=body)
        data = req.json()
        print(data)

        self.id = data['id']

    def ready_request(self, u):
        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=self.id), headers=self.header)
        req = req.json()
        self.req = req
        return req['done']

    def return_json(self):
        return self.req

    def return_text(self):
        strr = ''
        for chunk in self.req['response']['chunks']:
            strr = strr + str(chunk['alternatives'][0]['text'])
        return strr


class SynthesizeAudio:
    def __init__(self, key, catalogId):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": key}
        answer = requests.post(url, json=data)

        self.token = answer.json()['iamToken']
        self.catalogId = catalogId

    def __synthesizeStream__(self, text):
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {
            'Authorization': 'Bearer ' + self.token,
        }

        data = {
            'text': text,
            'lang': 'ru-RU',
            'folderId': self.catalogId,
            'voice': 'alena',
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError(
                    "Invalid response received: code: %d, message: %s" % (
                        resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk

    def synthesize(self, text, filepath):
        with open(filepath, "wb") as f:
            for audio_content in self.__synthesizeStream__(text):
                f.write(audio_content)

    def synthesize_stream(self, text):
        """
        : param io_stream: byttesIO object
        """
        audio_data = BytesIO()
        for audio_content in self.__synthesizeStream__(text):
            audio_data.write(audio_content)

        return audio_data
import requests
from os import system


class recognizeShortAudio:
    def __init__(self, key):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": key}
        answer = requests.post(url, json=data)

        # print(answer.json()['iamToken'])
        self.token = answer.json()['iamToken']


    def recognize(self, file, folder):
        url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId={}".format(folder)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        answer = requests.post(url, data=open(file, 'rb').read(), headers=headers)

        if answer.status_code != 200:
            raise Exception("It's error with recognizing: {}".format(response.json()))
        else:
            return answer.text


def recode (inputfile, outputfile):
    """Recodering file using ffmpeg

    :param inputfile: string, path to input file
    :param outputfile: string, path to output file
    """

    cmd = "ffmpeg -i '" + str(inputfile) + "' '" + str(outputfile) + "'"
    system(cmd)


class objectStorage:
    def __init__ (self, aws_access_key_id, aws_secret_access_key):
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
        return self.s3.upload_file(inputfilepath, baketname, outputfilename)


    def listObjectsInBucket(self, bucketname):
        return self.s3.list_objects(Bucket=bucketname)


    def deleteObject(self, object_name, bucketname):
        return self.s3.delete_objects(Bucket=bucketname, Delete={'Objects': [{'Key': object_name}]})


    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        try:
            response = self.s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

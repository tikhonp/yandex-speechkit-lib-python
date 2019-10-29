class recognize:


    def __init__(self, key):
        import requests
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": key}
        answer = requests.post(url, json=data)

        # print(answer.json()['iamToken'])
        self.token = answer.json()['iamToken']


    def recognize(self, file, folder):
        import requests
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
    from os import system
    cmd = "ffmpeg -i '" + str(inputfile) + "' '" + str(outputfile) + "'"
    system(cmd)

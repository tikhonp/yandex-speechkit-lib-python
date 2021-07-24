import speechkit
from sys import argv
from datetime import datetime
from time import sleep
import json

script, filename, outfilename, baketname = argv

objstrname = 'output_' + filename.split('/')[-1]

api_id = 'your api id here'
api_key = 'your api key here'

objectStorage = speechkit.ObjectStorage(
    aws_access_key_id=api_id, aws_secret_access_key=api_key)
objectStorage.upload_file(filename, baketname, objstrname)
urltofile = objectStorage.create_presigned_url(baketname, objstrname)

apiKey = 'your api key here'

recognizeLongAudio = speechkit.RecognizeLongAudio(apiKey)
recognizeLongAudio.send_for_recognition(urltofile)

while True:
    sleep(2)
    if recognizeLongAudio.get_recognition_results(): break
    print('recognizing ...')

output = recognizeLongAudio.get_data()

with open(outfilename, 'w') as outfile:
    json.dump(output, outfile, ensure_ascii=False, indent=2)

objectStorage.delete_object(objstrname, baketname)

print(recognizeLongAudio.get_raw_text())

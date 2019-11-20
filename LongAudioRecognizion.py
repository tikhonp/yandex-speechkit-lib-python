import speechkit
from sys import argv
from datetime import datetime
from time import sleep
import json

script, filename, outfilename, baketname = argv

objstrname = 'output' + str(str(str(datetime.now()).split(sep=' ')[1]).split(sep='.')[1]) + '.opus'
if speechkit.recode(filename, objstrname)!=0:
    raise Exception('RecoderingError')

api_id = "FPqJ7DjY0exB05saMLFo"
api_key = "IhFkcAfaoJgr4vF2FIOKpWXtClZrYO9MF5VKn9Wp"

objectStorage = speechkit.objectStorage(api_id, api_key)
objectStorage.upload_file(objstrname, baketname, objstrname)
urltofile = objectStorage.create_presigned_url(baketname, objstrname)


apiKey = 'AQVN3g4X20jg5vhLBtLnrVLmO3RCCLSEn_5OjjDQ'

recognizeLongAudio = speechkit.recognizeLongAudio(apiKey)
recognizeLongAudio.recognize_post(urltofile)

while True:
    sleep(2)
    if recognizeLongAudio.ready_request('j'): break
    print('recognizing ...')

output = recognizeLongAudio.return_list()

with open(outfilename, 'w') as outfile:
    json.dump(output, outfile)

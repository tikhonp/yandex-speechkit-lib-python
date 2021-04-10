import speechkit
from sys import argv
from datetime import datetime
from time import sleep
import json

script, filename, outfilename, baketname = argv

objstrname = 'output' + str(str(str(datetime.now()).split(sep=' ')[1]).split(sep='.')[1]) + '.opus'
if speechkit.recode(filename, objstrname)!=0:
    raise Exception('RecoderingError')

api_id = # your api id here
api_key = # your api key here

objectStorage = speechkit.objectStorage(api_id, api_key)
objectStorage.upload_file(objstrname, baketname, objstrname)
urltofile = objectStorage.create_presigned_url(baketname, objstrname)


apiKey = # your api key here

recognizeLongAudio = speechkit.recognizeLongAudio(apiKey)
recognizeLongAudio.recognize_post(urltofile)

while True:
    sleep(2)
    if recognizeLongAudio.ready_request('j'): break
    print('recognizing ...')

output = recognizeLongAudio.return_json()

with open(outfilename, 'w') as outfile:
    json.dump(output, outfile, ensure_ascii=False, indent=2)


objectStorage.deleteObject(objstrname, baketname)

for file in [filename, objstrname]:
    if speechkit.removefile(file)!=0:
        raise Exception('RemovingError')

from sys import argv
import time

import speechkit

_, filename = argv

api_key = os.environ.get('API_KEY')
service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
bucket_name = os.environ.get('BUCKET_NAME')
folder_id = os.environ.get('CATALOG')

if not api_key or not service_account_id or not bucket_name or not folder_id:
    print("Specify `API_KEY`, `SERVICE_ACCOUNT_ID`, `BUCKET_NAME`, `CATALOG` environment variables.")
    exit()

recognize_long_audio = speechkit.RecognizeLongAudio(api_key, service_account_id, bucket_name)
print("Sending file for recognition...")
recognize_long_audio.send_for_recognition(
    filename, audioEncoding='LINEAR16_PCM', sampleRateHertz='48000',
    audioChannelCount=1, rawResults=False
)
while True:
    time.sleep(2)
    if recognize_long_audio.get_recognition_results():
        break
    print("Recognizing...")

data = recognize_long_audio.get_data()
print("DATA:\n\n", data)

text = recognize_long_audio.get_raw_text()
print("TEXT:\n\n", text)

import time
from sys import argv

from speechkit import RecognitionLongAudio, Session
from speechkit.auth import generate_jwt

_, filename = argv

bucket_name = os.environ.get('BUCKET_NAME')
service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
key_id = os.environ.get('YANDEX_KEY_ID')
private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()

if not key_id or not service_account_id or not bucket_name or not private_key:
    print("Specify `YANDEX_KEY_ID`, `SERVICE_ACCOUNT_ID`, `BUCKET_NAME`, `private_key` environment variables.")
    exit()

jwt = generate_jwt(service_account_id, key_id, private_key)
session = Session.from_jwt(jwt)

recognize_long_audio = RecognitionLongAudio(session, service_account_id, bucket_name)

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

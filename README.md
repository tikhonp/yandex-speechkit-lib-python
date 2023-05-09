<div align="center">
  <br>
  <h1>🎙 Yandex SpeechKit Python SDK</h1>
  
  ![PyPI](https://img.shields.io/pypi/v/speechkit) ![GitHub](https://img.shields.io/github/license/tikhonp/yandex-speechkit-lib-python) ![build and test](https://github.com/TikhonP/yandex-speechkit-lib-python/actions/workflows/python-package.yml/badge.svg) [![Updates](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/shield.svg)](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/) [![codecov](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python/branch/master/graph/badge.svg?token=NRNV9E36I4)](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python) 
[![Documentation Status](https://readthedocs.org/projects/yandex-speechkit-lib-python/badge/?version=latest)](https://pip.pypa.io/en/stable/?badge=stable) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FTikhonP%2Fyandex-speechkit-lib-python.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FTikhonP%2Fyandex-speechkit-lib-python?ref=badge_shield)
[![Downloads](https://pepy.tech/badge/speechkit)](https://pepy.tech/project/speechkit)

</div>

Python SDK for Yandex SpeechKit API. This SDK allows you to use the cloud API for speech recognition and synthesis from Yandex. 

For more information please visit [Yandex Speechkit API Docs](https://cloud.yandex.com/en/docs/speechkit/). This lib
supports short and long audio recognition with speechkit

## 🛠 Getting Started

Assuming that you have Python and `virtualenv` installed, set up your environment and install the required dependencies
like this, or you can install the library using `pip`:

```sh
$ git clone https://github.com/TikhonP/yandex-speechkit-lib-python.git
$ cd yandex-speechkit-lib-python
$ virtualenv venv
...
$ . venv/bin/activate
$ python -m pip install -r requirements.txt
$ python -m pip install .
```

```sh
python -m pip install speechkit
```

## 📑 Speechkit documentation

Check out [speechkit docs](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html) for more
info. [PDF docs](https://yandex-speechkit-lib-python.readthedocs.io/_/downloads/en/latest/pdf/)

## 🔮 Using speechkit

There are support of recognizing long and short audio and synthesis. For more information please read docs below.

First you need create session for authorisation:

```python3
from speechkit import Session

oauth_token = str('<oauth_token>')
folder_id = str('<folder_id>')
api_key = str('<api-key>')
jwt_token = str('<jwt_token>')

oauth_session = Session.from_yandex_passport_oauth_token(oauth_token, folder_id)
api_key_session = Session.from_api_key(api_key, x_client_request_id_header=True, x_data_logging_enabled=True) 
# You can use `x_client_request_id_header` and `x_data_logging_enabled` params to troubleshoot yandex recognition
# Use `Session.get_x_client_request_id()` method to get x_client_request_id value.
jwt_session = Session.from_jwt(jwt_token)
```

Use created session to make other requests.

There are also functions for getting credentials (read [Documentation](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html) for more info):
`Speechkit.auth.generate_jwt`,  `speechkit.auth.get_iam_token`, `speechkit.auth.get_api_key`

### For audio recognition

Short audio:

```python3
from speechkit import ShortAudioRecognition

recognizeShortAudio = ShortAudioRecognition(session)
with open(str('/Users/tikhon/Desktop/out.wav'), str('rb')) as f:
    data = f.read()

print(recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz='48000'))

# Will be printed: 'text that need to be recognized'
```

Look at example with long
audio [long_audio_recognition.py](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/examples/long_audio_recognition.py)
.

Look at example with streaming
audio [streaming_recognize.py](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/examples/streaming_recognize.py)

### For synthesis

```python3
from speechkit import SpeechSynthesis

synthesizeAudio = SpeechSynthesis(session)
synthesizeAudio.synthesize(
    str('/Users/tikhon/Desktop/out.wav'), text='Text that will be synthesised',
    voice='oksana', format='lpcm', sampleRateHertz='16000'
)
```

## 🔗 Links

- [Readthedocs Documentation for this package](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html)
- [Yandex Speechkit Documentation](https://cloud.yandex.com/en/docs/speechkit/)
- [Статья на хабре](https://habr.com/ru/post/681566/)

## 💼 License

[MIT](LICENSE)

In other words, you can use the code for private and commercial purposes with an author attribution (by including the original license file).

❤️

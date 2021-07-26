# Yandex Speechkit Python SDK

![PyPI](https://img.shields.io/pypi/v/speechkit) ![GitHub](https://img.shields.io/github/license/tikhonp/yandex-speechkit-lib-python) ![PyPI - Format](https://img.shields.io/pypi/format/wheel) [![Build Status](https://travis-ci.com/TikhonP/yandex-speechkit-lib-python.svg?branch=master)](https://travis-ci.com/TikhonP/yandex-speechkit-lib-python) [![Updates](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/shield.svg)](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/) [![Python 3](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/python-3-shield.svg)](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/) [![codecov](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python/branch/master/graph/badge.svg?token=NRNV9E36I4)](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python)

Python SDK for Yandex Speechkit API.

For more information please visit [Yandex Speechkit API Docs](https://cloud.yandex.com/en/docs/speechkit/). This lib
supports short and long audio recognition of speechkit

# Getting Started

Assuming that you have Python and `virtualenv` installed, set up your environment and install the required dependencies
like this, or you can install the library using `pip`:

```bash
$ git clone https://github.com/TikhonP/yandex-speechkit-lib-python.git
$ cd yandex-speechkit-lib-python
$ virtualenv venv
...
$ . venv/bin/activate
$ python -m pip install -r requirements.txt
$ python -m pip install .
```

```bash
python -m pip install speechkit
```

## Using speechkit

There are support of recognizing long and short audio and synthesis. For more information please read docs below.

#### For short audio

From a Python interpreter:

```python3
import speechkit

recognizeShortAudio = speechkit.RecognizeShortAudio(str('<yandex_passport_oauth_token>'))
with open('/Users/tikhon/Desktop/out.wav', 'rb') as f:
    data = f.read()

print(recognizeShortAudio.recognize(data, folderId='<folder _id>', format='lpcm', sampleRateHertz='48000'))

'Текст который нужно распознать'
```

#### For synthesis

```python3
import speechkit

synthesizeAudio = speechkit.SynthesizeAudio(str('<yandex_passport_oauth_token>'))
synthesizeAudio.synthesize(str('/Users/tikhon/Desktop/out.wav'), text='Текст который нужно синтезировать',
                           voice='oksana', format='lpcm', sampleRateHertz='16000', folderId='<folder _id>')
```

#### For long audio

See [long_audio_recognition.py](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/examples/long_audio_recognition.py)

# Speechkit documentation

See [speechkit docs](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/DOCS.md) for more info.

# Todo

-

# License

Copyright 2021 Tikhon Petrishchev
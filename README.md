# speechkit lib python

It's lib for using speechkit api by yandex.
 
This lib supports short and long audio recognition of 
speechkit

## Install

```
pip install git+https://github.com/TikhonP/speechkit-lib-python.git
```
or

```
git clone https://github.com/TikhonP/speechkit-lib-python.git
sudo python setup.py install
```
 
## How to use

Import:

```python3
import speechkit
```

#### For short audio

Init:

```python3
spchkt = speechkit.RecognizeShortAudio(token)
```

Use token for getting iam

Recognize:
```python3
text = spchkt.recognize(filename, folder_id)
```
Please write folder_id

#### For long audio

For long audio you need to upload file to the yandex object storage. You can do it with objectStorage class:

```python3
objstor = speechkit.ObjectStorage(aws_access_key_id, aws_secret_access_key)
```

Speechkit works with ogg opus file. This function recoding audio with ffmpeg. It works only on unix system and you need to install ffmpeg.
```python3
out = speechkit.recode(infilename, outfilename)
```

It will save opus file to the same directory.

There is also supporting removing files by command rm <filename>
```python3
out = speechkit.removefile(inputfile)
```
 They return '0', if process was done successfully

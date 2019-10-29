# speechkit lib python
 It's lib for using speechkit api by yandex.

## How to use

#### Import:

```python3
import speechkit
```
#### Init:

```python3
spchkt = speechkit.recognize(token)
```

#### Use token for getting iam

#### Recognize:
```python3
text = spchkt.recognize(filename, folder_id)
```
#### Plese write folder_id

#### Speechkit works with ogg opus file. This function recoding audio with ffmpeg. It works only on unix system and you need to install ffmpeg.
```python3
speechkit.recode(infilename, outfilename)
```

#### It will save opus file to the same directory.

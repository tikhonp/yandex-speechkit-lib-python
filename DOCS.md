# speechkit package

## Module contents

speechkit
Python SDK for using Yandex Speech recognition and synthesis


### exception speechkit.InvalidDataError()
Bases: `ValueError`

Exception raised for errors when data not valid


### class speechkit.RecognizeLongAudio(yandex_passport_oauth_token, service_account_id, aws_bucket_name=None, aws_credentials_description='Default AWS credentials created by \`speechkit\` python SDK', aws_region_name='ru-central1')
Bases: `object`

Long audio fragment recognition can be used

    for multi-channel audio files up to 1 GB.

To recognize long audio fragments, you need to execute 2 requests:

    
    * Send a file for recognition.


    * Get recognition results.

    ```python
    >>> recognizeLongAudio = RecognizeLongAudio('<yandex_passport_oauth_token>', '<service_account_id>')
    >>> recognizeLongAudio.send_for_recognition('file/path')
    >>> if recognizeLongAudio.get_recognition_results():
    ...     data = recognizeLongAudio.get_data()
    ...
    >>> recognizeLongAudio.get_raw_text()
    'raw recognized text'
    ```

Initialize Api-Key for recognizing long audio


* **Parameters**

    **api_key** (*string*) – The API key is a private key used for simplified
    authorization in the Yandex.Cloud API.



* **Returns**

    __init__ should return None



* **Return type**

    None



#### get_data()
Get the response.
Use `RecognizeLongAudio.get_recognition_results()` first to store _answer_data

Contain a list of recognition results (chunks[]).


* **Returns**

    None if text not found ot Each result in the chunks[] list contains the following fields:


    * alternatives[]: List of recognized text alternatives. Each alternative contains the following fields:

    > 
    >     * words[]: List of recognized words:

    > > 
    > >         * startTime: Time stamp of the beginning of the word in the recording. An error of 1-2 seconds

    > >     is possible.


    > >         * endTime: Time stamp of the end of the word. An error of 1-2 seconds is possible.


    > >         * word: Recognized word. Recognized numbers are written in words (for example, twelve rather

    > >     than 12).


    > >         * confidence: This field currently isn’t supported. Don’t use it.


    > >         * text: Full recognized text. By default, numbers are written in figures. To output the entire

    > >     text in words, specify true in the raw_results field.


    > >         * confidence: This field currently isn’t supported. Don’t use it.


    * channelTag: Audio channel that recognition was performed for.




#### get_raw_text()
Get raw text from _answer_data data


* **Returns**

    Text



#### get_recognition_results()
Monitor the recognition results using the received ID.
The number of result monitoring requests is limited,
so consider the recognition speed: it takes about 10 seconds
to recognize 1 minute of single-channel audio.


#### send_for_recognition(file_path, \*\*kwargs)
Send a file for recognition


* **Parameters**

    
    * **file_path** (*string*) – Path to input file


    * **folder_id** (*string*) – ID of the folder that you have access to. Don’t specify this field if
    you make a request on behalf of a service account.


    * **languageCode** (*string*) – The language that recognition will be performed for.
    Only Russian is currently supported (ru-RU).


    * **model** (*string*) – The language model to be used for recognition.
    Default value: general.


    * **profanityFilter** (*boolean*) – The profanity filter.


    * **audioEncoding** (*string*) – The format of the submitted audio.
    Acceptable values:


        * LINEAR16_PCM: LPCM with no WAV _header.


        * OGG_OPUS (default): OggOpus format.



    * **sampleRateHertz** (*integer*) – The sampling frequency of the submitted audio.
    Required if format is set to LINEAR16_PCM. Acceptable values:


        * 48000 (default): Sampling rate of 48 kHz.


        * 16000: Sampling rate of 16 kHz.


        * 8000: Sampling rate of 8 kHz.



    * **audioChannelCount** (*integer*) – The number of channels in LPCM files.
    By default, 1. Don’t use this field for OggOpus files.


    * **rawResults** (*boolean*) – Flag that indicates how to write numbers.
    true: In words. false (default): In figures.



### class speechkit.RecognizeShortAudio(yandex_passport_oauth_token)
Bases: `object`

Short audio recognition ensures fast response time and is suitable for single-channel audio of small length.

Audio requirements:

    
    * Maximum file size: 1 MB.


    * Maximum length: 30 seconds.


    * Maximum number of audio channels: 1.

Gets IAM _token and stores in RecognizeShortAudio._token


* **Parameters**

    **yandex_passport_oauth_token** (*string*) – OAuth _token from Yandex.OAuth



* **Returns**

    __init__ should return None



* **Return type**

    None



#### recognize(data, \*\*kwargs)
Recognize text from BytesIO data given, which is audio


* **Parameters**

    
    * **data** (*io.BytesIO**, **bytes*) – Data with audio samples to recognize


    * **lang** (*string*) – The language to use for recognition. Acceptable values:


        * ru-RU (by default) — Russian.


        * en-US — English.


        * tr-TR — Turkish.



    * **topic** (*string*) – The language model to be used for recognition. Default value: general.


    * **profanityFilter** (*boolean*) – This parameter controls the profanity filter in recognized speech.


    * **format** (*string*) – The format of the submitted audio. Acceptable values:


        * lpcm — LPCM with no WAV _header.


        * oggopus (default) — OggOpus.



    * **sampleRateHertz** (*string*) – The sampling frequency of the submitted audio.
    Used if format is set to lpcm. Acceptable values:


        * 48000 (default) — Sampling rate of 48 kHz.


        * 16000 — Sampling rate of 16 kHz.


        * 8000 — Sampling rate of 8 kHz.




* **Returns**

    The recognized text



* **Return type**

    string



### exception speechkit.RequestError(answer: dict, \*args)
Bases: `Exception`

Exception raised for errors while yandex api request


### class speechkit.SynthesizeAudio(yandex_passport_oauth_token)
Bases: `object`

Generates speech from received text.


* **Parameters**

    **yandex_passport_oauth_token** (*string*) – OAuth _token from Yandex.OAuth



#### synthesize(file_path, \*\*kwargs)
Generates speech from received text and saves it to file


* **Parameters**

    
    * **file_path** (*string*) – The path to file where store data


    * **text** (*string*) – UTF-8 encoded text to be converted to speech.
    You can only use one text and ssml field.
    For homographs, place a + before the stressed vowel.
    For example, contr+ol or def+ect.
    To indicate a pause between words, use -.
    Maximum string length: 5000 characters.


    * **ssml** (*string*) – Text in SSML format to be converted into speech.
    You can only use one text and ssml fields.


    * **lang** (*string*) – Language.
    Acceptable values:


        * ru-RU (default) — Russian.


        * en-US — English.


        * tr-TR — Turkish.



    * **voice** (*string*) – Preferred speech synthesis voice from the list.
    Default value: oksana.


    * **speed** (*string*) – Rate (speed) of synthesized speech.
    The rate of speech is set as a decimal number in the range from 0.1 to 3.0. Where:


        * 3.0 — Fastest rate.


        * 1.0 (default) — Average human speech rate.


        * 0.1 — Slowest speech rate.



    * **format** (*string*) – The format of the synthesized audio. Acceptable values:
    \* lpcm — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

    > 
    >     * Sampling — 8, 16, or 48 kHz, depending on the value of the sampleRateHertz parameter.


    >     * Bit depth — 16-bit.


    >     * Byte order — Reversed (little-endian).


    >     * Audio data is stored as signed integers.


        * oggopus (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using

        the OGG container format (OggOpus).



    * **folderId** (*string*) – ID of the folder that you have access to.
    Required for authorization with a user account (see the UserAccount resource).
    Don’t specify this field if you make a request on behalf of a service account.



#### synthesize_stream(\*\*kwargs)
Generates speech from received text and return io.BytesIO object

    with data.


* **Parameters**

    
    * **text** (*string*) – UTF-8 encoded text to be converted to speech.
    You can only use one text and ssml field.
    For homographs, place a + before the stressed vowel.
    For example, contr+ol or def+ect.
    To indicate a pause between words, use -.
    Maximum string length: 5000 characters.


    * **ssml** (*string*) – Text in SSML format to be converted into speech.
    You can only use one text and ssml fields.


    * **lang** (*string*) – Language.
    Acceptable values:


        * ru-RU (default) — Russian.


        * en-US — English.


        * tr-TR — Turkish.



    * **voice** (*string*) – Preferred speech synthesis voice from the list.
    Default value: oksana.


    * **speed** (*string*) – Rate (speed) of synthesized speech.
    The rate of speech is set as a decimal number in the range from 0.1 to 3.0. Where:


        * 3.0 — Fastest rate.


        * 1.0 (default) — Average human speech rate.


        * 0.1 — Slowest speech rate.



    * **format** (*string*) – The format of the synthesized audio. Acceptable values:
    \* lpcm — Audio file is synthesized in LPCM format with no WAV _header. Audio properties:

    > 
    >     * Sampling — 8, 16, or 48 kHz, depending on the value of the sampleRateHertz parameter.


    >     * Bit depth — 16-bit.


    >     * Byte order — Reversed (little-endian).


    >     * Audio data is stored as signed integers.


        * oggopus (default) — Data in the audio file is encoded using the OPUS audio codec and compressed using

        the OGG container format (OggOpus).



    * **sampleRateHertz** (*string*) – The sampling frequency of the synthesized audio.
    Used if format is set to lpcm. Acceptable values:


        * 48000 (default): Sampling rate of 48 kHz.


        * 16000: Sampling rate of 16 kHz.


        * 8000: Sampling rate of 8 kHz.



    * **folderId** (*string*) – ID of the folder that you have access to.
    Required for authorization with a user account (see the UserAccount resource).
    Don’t specify this field if you make a request on behalf of a service account.



### speechkit.get_api_key(yandex_passport_oauth_token: Optional[str] = None, service_account_id: Optional[str] = None, description: str = 'Default Api-Key created by \`speechkit\` python SDK')
Creates an API key for the specified service account.


### speechkit.get_iam_token(yandex_passport_oauth_token: Optional[str] = None, jwt: Optional[str] = None)
Creates an IAM token for the specified identity.


### speechkit.list_of_service_accounts(yandex_passport_oauth_token, folder_id, \*\*kwargs)
Retrieves the list of ServiceAccount resources in the specified folder.

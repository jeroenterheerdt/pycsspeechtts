# pycsspeechtts
Python (py) library to use Microsofts Cognitive Services Speech (csspeech) Text to Speech (tts) API.
The cryptic name is the combination of the abbrevations shown above.

Usage:
```python
from pycsspeechtts import TTSTranslator
t = TTSTranslator("YOUR API KEY")
data = t.speak('en-gb','Male','I am Max', 'George, Apollo', 'audio-16khz-128kbitrate-mono-mp3')
```

See test.py for more samples.
Refer to https://docs.microsoft.com/en-us/azure/cognitive-services/Speech/api-reference-rest/bingvoiceoutput to find the valid values for language, gender, voicetype and output formats.
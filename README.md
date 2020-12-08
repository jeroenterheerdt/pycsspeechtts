# pycsspeechtts
Python (py) library to use Microsofts Cognitive Services Speech (csspeech) Text to Speech (tts) API.
The cryptic name is the combination of the abbrevations shown above.

Usage:
```python
from pycsspeechtts import TTSTranslator
t = TTSTranslator("YOUR API KEY","westeurope")

data = t.speak(text='The default voice is using Microsoft Neural Voice. When using a neural voice, synthesized speech is nearly indistinguishable from the human recordings.')
with open("file1.wav", "wb") as f:
        f.write(data)

data = t.speak('en-gb','Male','I am Max', 'George, Apollo', 'riff-16khz-16bit-mono-pcm', text='I am Max')
with open("file2.wav", "wb") as f:
        f.write(data)
```

You can also use custom voice by specifying `isCustom=True` and providing a `customEndpoint`:
```python
from pycsspeechtts import TTSTranslator
t = TTSTranslator("YOUR API KEY","westeurope", isCustom=True, customEndpoint=MyEndpoint)
data = t.speak(language='en-gb',gender='Male',voiceType="ArchieNeural",text="This is a test for custom voice")
```

See test.py for more samples.
Refer to https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support to find the valid values for language, gender, voicetype and output formats.
from pycsspeechtts import TTSTranslator
t = TTSTranslator("YOUR API KEY")

#Speaking with default language of english US and default Female voice
data = t.speak(text='This is a test')
#Change speed with -50%
data = t.speak(text="This is a test",rate="-50%")
#Change pitch to high
data = t.speak(text="This is a test",pitch="high")
#Change volume to +20%
data = t.speak(text="This is a test",volume="+20%")
#Using contour to change pitch from normal at 0% of speech and +100% at 100% of speech
data = t.speak(text="This is a test",contour="(0%,+0%) (100%,+100%)")
#See https://docs.microsoft.com/en-us/azure/cognitive-services/Speech/api-reference-rest/bingvoiceoutput for the accepted values of the parameters below
data = t.speak('en-gb','Male', 'George, Apollo', 'audio-16khz-128kbitrate-mono-mp3', 'I am Max')


if data == None:
    print("An error occured")
else: 
    with open ("file.wav","wb") as f:
        f.write(data)
    print("Succes! Open file.wav to hear the results")
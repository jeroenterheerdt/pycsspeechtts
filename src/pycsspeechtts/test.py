from pycsspeechtts import TTSTranslator
t = TTSTranslator("YOUR API KEY")


data = t.speak(text='This is a test')
#See https://docs.microsoft.com/en-us/azure/cognitive-services/Speech/api-reference-rest/bingvoiceoutput for the accepted values of the parameters below
data = t.speak('en-gb','Male', 'George, Apollo', 'audio-16khz-128kbitrate-mono-mp3', 'I am Max')

if data == None:
    print("An error occured")
else: 
    with open ("file.wav","wb") as f:
        f.write(data)
    print("Succes! Open file.wav to hear the results")
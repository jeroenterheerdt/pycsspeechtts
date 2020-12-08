from pycsspeechtts import TTSTranslator
useCustom = True
api_key = "YOUR_API_KEY"
custom_endpoint = "custom_endpoint"

if not useCustom:
    t = TTSTranslator(api_key, region="westus")
    # Speaking with default language of english US and default Female voice
    data = t.speak(text='This is a test')
    # Change speed with -50%
    data = t.speak(text="This is a test", rate="-50%")
    # Change pitch to high
    data = t.speak(text="This is a test", pitch="high")
    # Change volume to +20%
    data = t.speak(text="This is a test", volume="+20%")
    # See https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support for the accepted values of the parameters below
    data = t.speak('en-GB', 'Male', 'George, Apollo',
                'riff-16khz-16bit-mono-pcm', text='I am Max')
    data = t.speak('cs-CZ', 'Male', 'Jakub', text='Pojďme vyzkoušet klasickou českou testovací větu. Příliš žluťoučký kůň úpěl ďábelské ódy.')
    # Using contour to change pitch from normal at 0% of speech and +100% at 100% of speech
    data = t.speak(text="The Wall Street Journal - which says it's spoken to people close to the ongoing investigation - says the information it has paints a picture of a catastrophic failure that quickly overwhelmed the flight crew",
                contour="(0%,+0%) (100%,+100%)")
else:
    # Test custom voice
    t = TTSTranslator(api_key, region="westus", isCustom=True, customEndpoint=custom_endpoint)
    data = t.speak(language='en-gb',gender='Male',voiceType="ArchieNeural",text="This is a test for custom voice")

if data == None:
    print("An error occurred")
else:
    with open("file.wav", "wb") as f:
        f.write(data)
    print("Success! Open file.wav to hear the results")

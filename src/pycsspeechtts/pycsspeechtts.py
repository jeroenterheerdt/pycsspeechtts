"""
Python wrapper for Microsoft Cognitive Services Text-to-speech translator
"""
import requests
import json
from xml.etree import ElementTree
import logging
import sys

_LOGGER = logging.getLogger(__name__)

AccessTokenUrlTemplate = "https://{}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
SpeechUrlTemplate = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1"

class TTSTranslator(object):
    """
    Interface class for the Microsoft Cognitive Services Text-to-speech translator
    """

    def __init__(self, apiKey, region="eastus"):
        self._apiKey = apiKey
        self._geoLocation = region

        headers = {"Ocp-Apim-Subscription-Key": self._apiKey}
        response = requests.post(AccessTokenUrlTemplate.format(
            self._geoLocation), headers=headers)
        response.raise_for_status()
        _LOGGER.debug("Connection Initialized OK")
        self._accesstoken = str(response.text)

    def speak(self, language="en-us", gender="Female", voiceType="JessaNeural",
              output="riff-24khz-16bit-mono-pcm", rate="+0.00%", volume="+0.00%",
              pitch="default", contour="(0%,+0%) (100%,+0%)", text=None):
        def name_lang(language):
            lang1,lang2 = language.split("-")
            return "{}-{}".format(lang1,lang2.upper())
        
        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', language)

        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice ('+name_lang(language)+', '+voiceType+')')

        prosody = ElementTree.SubElement(voice, 'prosody')
        prosody.set('rate', rate)
        prosody.set('volume', volume)
        prosody.set('pitch', pitch)
        prosody.set('contour', contour)
        prosody.text = text

        headers = {"Content-Type": "application/ssml+xml",
                   "X-Microsoft-OutputFormat": output,
                   "Authorization": "Bearer " + self._accesstoken,
                   "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                   "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                   "User-Agent": "PYCSSpeechTTS"
                   }

        response = requests.post(
            SpeechUrlTemplate.format(self._geoLocation), ElementTree.tostring(body), headers=headers)
        if response.status_code == requests.codes.ok:
            _LOGGER.debug("Text synthesis OK")
            return response.content
        else:
            _LOGGER.error("Text synthesis failed, statuscode " +
                          str(response.status_code)+", reason: "+response.text)
            return None

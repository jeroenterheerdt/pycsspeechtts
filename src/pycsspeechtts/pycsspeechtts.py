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

    def __init__(self, apiKey, region="eastus", isCustom=False, customEndpoint=None):
        self._apiKey = apiKey
        self._geoLocation = region
        self._isCustom = isCustom
        self._customEndpoint=customEndpoint

        headers = {"Ocp-Apim-Subscription-Key": self._apiKey}
        if not self._isCustom:
            response = requests.post(AccessTokenUrlTemplate.format(
                self._geoLocation), headers=headers)
            response.raise_for_status()
            self._accesstoken = str(response.text)
        _LOGGER.debug("Connection Initialized OK")
        

    def speak(self, language="en-us", gender="Female", voiceType="JessaNeural",
              output="riff-24khz-16bit-mono-pcm", rate="+0.00%", volume="+0.00%",
              pitch="default", contour="(0%,+0%) (100%,+0%)", text=None):
        def name_lang(language):
            parts = language.split("-", 1)
            lang1 = parts[0]
            lang2 = parts[1]

            subparts = lang2.split("-", 1)
            subpart1 = subparts[0].upper()
            subpart2 = subparts[1] if len(subparts) > 1 else ""

            return "{}-{}-{}".format(lang1, subpart1, subpart2).rstrip("-")
        
        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        body.set('xmlns','http://www.w3.org/2001/10/synthesis')
        body.set('xmlns:mstts', 'http://www.w3.org/2001/mstts')

        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice ('+name_lang(language)+', '+voiceType+')')

        endpoint = None
        if self._isCustom:
            # this is a custom voice
            endpoint = self._customEndpoint
            headers = {"Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": output,
                "Ocp-Apim-Subscription-Key": self._apiKey,
                "User-Agent": "PYCSSpeechTTS"
                }
            voice.text = text
        else: 
            # not a custom voice, generate the endpoint
            endpoint = SpeechUrlTemplate.format(self._geoLocation)
            headers = {"Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": output,
                "Authorization": "Bearer " + self._accesstoken,
                "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                "User-Agent": "PYCSSpeechTTS"
                }
            voice.append(ElementTree.XML('<prosody>'+text+'</prosody>'))
            prosody = voice.find('prosody')
            prosody.set('rate', rate)
            prosody.set('volume', volume)
            prosody.set('pitch', pitch)
            prosody.set('contour', contour)

        response = requests.post(
            endpoint, ElementTree.tostring(body), headers=headers)
        if response.status_code == requests.codes.ok:
            _LOGGER.debug("Text synthesis OK")
            return response.content
        else:
            _LOGGER.error("Text synthesis failed, statuscode " +
                          str(response.status_code)+", reason: "+response.text)
            return None

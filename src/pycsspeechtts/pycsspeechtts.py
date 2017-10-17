"""
Python wrapper for Microsoft Cognitive Services Text-to-speech translator
"""

import http.client, urllib.parse, json
from xml.etree import ElementTree
import logging

_LOGGER = logging.getLogger(__name__)

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

SpeechHost = "speech.platform.bing.com"


class TTSTranslator(object):
    """
    Interface class for the Microsoft Cognitive Services Text-to-speech translator
    """
    def __init__(self, apiKey):
        self._apiKey = apiKey
        conn = http.client.HTTPSConnection(AccessTokenHost)
        headers = {"Ocp-Apim-Subscription-Key":self._apiKey}
        conn.request("POST",path,"",headers)
        response = conn.getresponse()
        if response.status == 200:
            _LOGGER.debug("Connection Initialized OK")
            data = response.read()
            self._accesstoken = data.decode("UTF-8")
        else:
            _LOGGER.debug("Connection Intialization failed, statuscode "+str(response.status)+", reason: "+response.reason)
        conn.close()

    def speak(self, language="en-us", gender="Female", voiceType="ZiraRUS", output="riff-16khz-16bit-mono-pcm", text=None):
        body = ElementTree.Element('speak',version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang',language)
        voice = ElementTree.SubElement(body,'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang',language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender',gender)
        voice.set('name','Microsoft Server Speech Text to Speech Voice ('+language+', '+voiceType+')')
        voice.text = text
        headers = {"Content-Type": "application/ssml+xml",
                    "X-Microsoft-OutputFormat": output,
                    "Authorization": "Bearer " + self._accesstoken,
                    "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			        "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                    "User-Agent": "PYCSSpeechTTS"
        }

        conn = http.client.HTTPSConnection(SpeechHost)
        conn.request("POST","/synthesize",ElementTree.tostring(body),headers)
        response = conn.getresponse()
        if response.status == 200:
            _LOGGER.debug("Text synthesis OK")
            data = response.read()
            return data
        else:
            _LOGGER.debug("Text synthesis failed, statuscode "+str(response.status)+", reason: "+response.reason)
            return None
        conn.close()
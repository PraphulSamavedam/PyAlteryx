import hmac
from time import time
from random import choice
from string import ascii_letters
import requests
from urllib.parse import urlencode, quote
from hashlib import sha1

class AlteryxGalleryConnection:
    def __init__(self, api_key:str, secret:str, api_url:str):
        """ Parameters required for the Gallery connection  while initializing
         :arg api_key: str "Obtain this information under your account settings
         :arg secret: str "Obtain this information under your account settings
         :arg api_url: str "This is the url fo the api
        """
        self.api_key = api_key
        self.api_secret = secret
        if api_url.endswith('/api/v1/'):
            self.api_url = api_url
        elif api_url.endswith('/api/v1'):
            self.api_url = api_url + "/"
        elif api_url.endswith('/api'):
            self.api_url = api_url + "/v1/"
        elif api_url.endswith('/api/'):
            self.api_url = api_url + "v1/"
        else:
            print("api_url must end with (/api/v1/,/api,/api/,/api/v1)\napi_url provided endswith "
                  f"{api_url.endswith(start=len(api_url)-8)}")
            raise ValueError

    def getOAuthparams(self, http_method:str, url:str) -> dict:
        params = dict()
        params['oauth_signature_method'] = 'HMAC-SHA1'
        params['oauth_version'] = '1.0'
        params['oauth_consumer_key'] = self.api_key
        params['oauth_timestamp'] = str(int(time()))
        params['oauth_nonce'] = "".join(choice(ascii_letters) for x in range(5))
        params['signature'] = self._generate_signature(http_method=http_method, url= url, params=params)
        return  params

    def getWorkFlowsUnderSubscription(self):
        """Obtains the workflows under the subscription"""
        url = self.api_url + "workflows/subscription/"
        params = self.__getOAuthparams()
        output = requests.get(url=url, params=params)
        return output

    def _generate_signature(self, http_method:str, url:str,params:dict):
        byte_encoded_secret = bytearray(self.api_secret,encoding='UTF-8')
        raw_d = urlencode(params)
        encoded_header = urlencode(params, safe='~', quote_via=quote)
        encoded_url = urlencode(params, safe='~', quote_via=quote)
        encoded_msg =  "&".join(http_method.upper(),encoded_url,encoded_header)
        hmac_encoded = hmac.new(key=byte_encoded_secret,msg=encoded_msg,digestmod=sha1)
        return hmac_encoded.digest().encode('base64').rstrip('\n')



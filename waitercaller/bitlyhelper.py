from urllib.request import urlopen
import json

TOKEN = "d170a7f79984f22a17e1cd98917c0dac52481997"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urlopen(url).read().decode('utf8')
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print(e)

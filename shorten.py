import requests
from decouple import config

def shorten(link,title):
    headers = {'Content-Type': 'application/json',"Authorization":config('BITLY_TOKEN')}
    payload = {'long_url': link,'title':title}
    r = requests.post("https://api-ssl.bitly.com/v4/bitlinks", json=payload,headers=headers)
    return r.json()["link"]
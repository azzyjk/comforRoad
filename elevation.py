import requests
import json
import pprint

readG = open('gmapKey.txt', mode='rt', encoding='utf-8')
key = readG.read()

url = 'https://maps.googleapis.com/maps/api/elevation/json'

params = {'locations':'37.390458, 126.956167',
		  'key':key
		  }

res = requests.get(url, params=params)

pprint.PrettyPrinter(indent=4).pprint(res.json())
import requests
import json
import pprint
import time

readT = open('tmapKey.txt', mode='rt', encoding='utf-8')
key = readT.read()

url = 'https://apis.openapi.sk.com/tmap/pois/search/around'

params = {'version':'1', 
		   'centerLon':'127.070974',
		  'centerLat':'37.540380',
		  'page':'1',
		  'count':'5',
		 # 'categories':'편의점;한식;한의원',
		  'appKey':key
		  }

res = requests.get(url, params=params)

for i in res.json()['searchPoiInfo']['pois']['poi']:
	print(i['name'], i['frontLat'], i['frontLon'])
#pprint.PrettyPrinter(indent=4).pprint(res.json())

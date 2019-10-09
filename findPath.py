import requests
import json
import pprint
import time

readT = open('tmapKey.txt', mode='rt', encoding='utf-8')
key = readT.read()

url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1'

params = {'startX':'126.956167', 
		   'startY':'37.390458',
		  'speed':'300',
		   'endX':'126.956971', 
		   'endY':'37.393164',
		   'startName':'%EC%B6%9C%EB%B0%9C',
		   'endName':'%EB%B3%B8%EC%82%AC',
		  'appKey':key
		  }

res = requests.post(url, data=params)

for i in res.json()['features']:
	pprint.PrettyPrinter(indent=4).pprint(res.json()['features'])
	#pprint.PrettyPrinter(indent=4).pprint(type(i['geometry']['coordinates'][0]))
	#if type(i['geometry']['coordinates'][0]) == float :
	#	print("true")

	#res.json['features'][0]['properties']
	#pprint.PrettyPrinter(indent=4).pprint(res.json()['features'])
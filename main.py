import requests
import json
import pprint
import time

#make udf to make gparams
readT = open('tmapKey.txt', mode='rt', encoding='utf-8')
keyT = readT.read()

readG = open('gmapKey.txt', mode='rt', encoding='utf-8')
keyG = readG.read()

Turl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1'
Gurl = 'https://maps.googleapis.com/maps/api/elevation/json'

#Tmap parameters
Tparams = {'startX':'126.956167', 
		   'startY':'37.390458',
		  'speed':'300',
		   'endX':'126.956971', 
		   'endY':'37.393164',
		   'startName':'%EC%B6%9C%EB%B0%9C',
		   'endName':'%EB%B3%B8%EC%82%AC',
		   'appKey':keyT
		  }

#Gmap parameters
Gparams = {'locations':'37.390458, 126.956167',
		  'key':keyG
		  }

#find the path
Tres = requests.post(Turl, data=params)

for i in Tres.json()['features']:
	pprint.PrettyPrinter(indent=4).pprint(i['geometry']['coordinates'][0])
	

res = requests.get(Gurl, params=params)

pprint.PrettyPrinter(indent=4).pprint(Gres.json())
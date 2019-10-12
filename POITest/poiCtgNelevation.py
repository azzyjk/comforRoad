import requests
import json
import pprint
import time

def mkTmapKey():
	read = open('tmapKey.txt', mode='rt', encoding='utf-8')
	key = read.read()
	return key
	
def mkGmapKey():
	read = open('gmapKey.txt', mode='rt', encoding='utf-8')
	key = read.read()
	return key

def mkGpara(x, y):
	params = {'locations':str(y)+", "+str(x),
		  	   'key':Gkey
			  }
	return params

Turl = 'https://apis.openapi.sk.com/tmap/pois/search/around'
Gurl = 'https://maps.googleapis.com/maps/api/elevation/json'
Tkey = mkTmapKey()
Gkey = mkGmapKey()

params = {'version':'1', 
		   'centerLon':'127.070974',
		  'centerLat':'37.540380',
		  'page':'1',
		  'count':'5',
		 # 'categories':'편의점;한식;한의원',
		  'appKey':Tkey
		  }

Tres = requests.get(Turl, params=params)

for i in Tres.json()['searchPoiInfo']['pois']['poi']:
	Gparams = mkGpara(i['frontLon'], i['frontLat'])
	Gres = requests.get(Gurl, params=Gparams)
	print(i['name'], Gres.json()['results'][0]['elevation'])


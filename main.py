import requests
import json
import pprint
import time

def average(lists):
	return sum(lists) / len(lists)

def mkKey(site):
	if site == 0:
		key = open('tmapKey.txt', mode='rt', encoding='utf-8')

	if site == 1:
		key = open('gmapKey.txt', mode='rt', encoding='utf-8')
		
	return key.read()

def mkElepara(lon, lat, key):
	params = {'locations':str(lat)+", "+str(lon),
		  	   'key':key
			  }
	return params

def mkTparaArnd(lon, lat, key):
	params = {'version':'1', 
		   'centerLon':lon,
		  'centerLat':lat,
		  'page':'1',
		  'count':'5',
		 # 'categories':'편의점;한식;한의원',
		  'appKey':key
		  }
	return params

def mkTparaPth(key):
	params = {'version':'1',
			'startX':'126.956167', 
		   'startY':'37.390458',
		  'speed':'300',
		   'endX':'126.956971', 
		   'endY':'37.393164',
		   'startName':'%EC%B6%9C%EB%B0%9C',
		   'endName':'%EB%B3%B8%EC%82%AC',
		   'appKey':key
		  }
	return params

def findElevation(listPath, url, key):
	lists = []
	
	for i in listPath:
		params = mkElepara(i[0], i[1], key)

		res = requests.get(url, params=params)
		lists.append(res.json()['results'][0]['elevation'])
	return lists
#basic setting
SKT=0
GOOGLE=1

pthUrl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
arndUrl = 'https://apis.openapi.sk.com/tmap/pois/search/around'
eleUrl = 'https://maps.googleapis.com/maps/api/elevation/json'

Tkey = mkKey(SKT)
Gkey = mkKey(GOOGLE)

listPath = []
listRoad = []

#Tmap find Path parameters
pthParams = mkTparaPth(Tkey)

#find path
resPth = requests.post(pthUrl, data=pthParams)

#save location's lon&lat in list
for i in resPth.json()['features']:
	if type(i['geometry']['coordinates'][0]) == float :
		listPath.append(i['geometry']['coordinates'])

#find elevation
listEle = findElevation(listPath, eleUrl, Gkey)

#Tmap around search parameters(max elevation location)
arndParams = mkTparaArnd(listPath[listEle.index(max(listEle))][0],listPath[listEle.index(max(listEle))][1], Tkey)

#search around max elevation location
resArnd = requests.get(arndUrl, params=arndParams)

#Around location about max elevation location
for i in resArnd.json()['searchPoiInfo']['pois']['poi']:
	eleParams = mkElepara(i['frontLon'], i['frontLat'], Gkey)
	resEle = requests.get(eleUrl, params=eleParams)
	listRoad.append(resEle.json()['results'][0]['elevation'])
print(listRoad)
	#print(i['name'], resEle.json()['results'][0]['elevation'])


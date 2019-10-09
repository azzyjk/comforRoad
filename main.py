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

def mkGpara(lon, lat, key):
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

#basic setting
pthUrl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
arndUrl = 'https://apis.openapi.sk.com/tmap/pois/search/around'
eleUrl = 'https://maps.googleapis.com/maps/api/elevation/json'
Tkey = mkTmapKey()
Gkey = mkGmapKey()

listPath = []
listEle = []

#Tmap find Path parameters
pthParams = mkTparaPth(Tkey)

#find path
resPth = requests.post(pthUrl, data=pthParams)

#save location's lon&lat in list
for i in resPth.json()['features']:
	if type(i['geometry']['coordinates'][0]) == float :
		listPath.append(i['geometry']['coordinates'])

#find elevation
for i in listPath:
	eleParams = mkGpara(i[0], i[1], Gkey)

	resEle = requests.get(eleUrl, params=eleParams)
	listEle.append(resEle.json()['results'][0]['elevation'])
		
#print("Max elevation :", max(listEle), "Min elevation :", min(listEle))

#print(listEle.index(max(listEle)))

#Tmap around search parameters(max elevation location)
arndParams = mkTparaArnd(listPath[listEle.index(max(listEle))][0],listPath[listEle.index(max(listEle))][1], Tkey)

#search around max elevation location
resArnd = requests.get(arndUrl, params=arndParams)

#Around location about max elevation location
for i in resArnd.json()['searchPoiInfo']['pois']['poi']:
	eleParams = mkGpara(i['frontLon'], i['frontLat'], Gkey)
	resEle = requests.get(eleUrl, params=eleParams)
	print(i['name'], resEle.json()['results'][0]['elevation'])


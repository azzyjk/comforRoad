import requests
import json
import pprint
import time

def mkGP(x, y):
	Gparams = {'locations':str(y)+", "+str(x),
		  	   'key':keyG
			  }
	return Gparams

#make udf to make gparams
readT = open('tmapKey.txt', mode='rt', encoding='utf-8')
keyT = readT.read()

readG = open('gmapKey.txt', mode='rt', encoding='utf-8')
keyG = readG.read()

Turl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
Gurl = 'https://maps.googleapis.com/maps/api/elevation/json'

listPath = []
listEle = []

#Tmap parameters
Tparams = {'version':'1',
			'startX':'126.956167', 
		   'startY':'37.390458',
		  'speed':'300',
		   'endX':'126.956971', 
		   'endY':'37.393164',
		   'startName':'%EC%B6%9C%EB%B0%9C',
		   'endName':'%EB%B3%B8%EC%82%AC',
		   'appKey':keyT
		  }

#find the path
Tres = requests.post(Turl, data=Tparams)

for i in Tres.json()['features']:
	if type(i['geometry']['coordinates'][0]) == float :
		listPath.append(i['geometry']['coordinates'])

#find elevation
for i in listPath:
	Gparams = mkGP(i[0], i[1])

	Gres = requests.get(Gurl, params=Gparams)
	listEle.append(Gres.json()['results'][0]['elevation'])
	pprint.PrettyPrinter(indent=4).pprint(Gres.json()['results'][0]['elevation'])
	
print("Max elevation :", max(listEle), "Min elevation :", min(listEle))


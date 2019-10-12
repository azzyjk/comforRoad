import requests
import json
import pprint
import time
import os

def mkPoiPara(address):
	params = {'version':'1', 
		  'count':'5',
		   'searchKeyword':address, 
		   'appKey':key
		  }
	return params

def mkPathParams(stX, stY, edX, edY):
	params = {'startX':stX, 
		   'startY':stY,
		  'speed':'300',
		   'endX':edX, 
		   'endY':edY,
		   'startName':'%EC%B6%9C%EB%B0%9C',
		   'endName':'%EB%B3%B8%EC%82%AC',
			'appKey':key
		  }
	return params

def search(add, param):
	res = requests.get(poiUrl, params=param)
	number = 0
	for i in res.json()['searchPoiInfo']['pois']['poi']:
		print("%d. " %number, i['name'] )
		number+=1
		
	choose = input("번호를 선택해주세요 : ")
	return int(choose), res

pathUrl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1'
poiUrl = 'https://apis.openapi.sk.com/tmap/pois'

readT = open('/workspace/Python_test/final/Tmap/Test/txtFiles/tmapKey.txt', mode='rt', encoding='utf-8')
key = readT.read()



os.system("clear")

addSt = input("출발지 : ")

params = mkPoiPara(addSt)
chSt, resSt = search(addSt, params)

stX = resSt.json()['searchPoiInfo']['pois']['poi'][chSt]['frontLon']
stY = resSt.json()['searchPoiInfo']['pois']['poi'][chSt]['frontLat']

os.system("clear")

addEd = input("도착지 : ")

params = mkPoiPara(addEd)
chEd, resEd = search(addSt, params)

os.system("clear")

edX = resEd.json()['searchPoiInfo']['pois']['poi'][chEd]['frontLon']
edY = resEd.json()['searchPoiInfo']['pois']['poi'][chEd]['frontLat']

pathParams = mkPathParams(stX, stY, edX, edY)

res = requests.post(pathUrl,data=pathParams)

for i in res.json()['features'] :
	x = "turnType" in i['properties']
	y = "time" in i['properties']
	if(x==True):
		direct = i['properties']['turnType']
		if direct==12 or direct==212:
			print('left')
		elif direct==13 or direct==213:
			print('right')	
		elif direct==16 or direct==214:
			print('8시')
		elif direct==17 or direct==215:
			print('10시')
		elif direct==18 or direct==216:
			print('2시')
		elif direct==19 or direct==217:
			print('4시')
		else:
			print('straight')
			
	if(y==True):
		delayTime = i['properties']['time']
		#time.sleep(delayTime/10)

#pprint.PrettyPrinter(indent=4).pprint(resSt.json()['searchPoiInfo']['pois']['poi'])

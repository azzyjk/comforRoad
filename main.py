import requests
import json
import pprint
import time
import os

def average(lists):
	return sum(lists) / len(lists)

def mkKey(site):
	if site == 0:
		key = open('/workspace/Python_test/final/Tmap/Test/txtFiles/tmapKey.txt', mode='rt', encoding='utf-8')

	if site == 1:
		key = open('/workspace/Python_test/final/Tmap/Test/txtFiles/gmapKey.txt', mode='rt', encoding='utf-8')
		
	return key.read()

def mkElepara(lon, lat, key):
	params = {'locations':str(lat)+", "+str(lon),
		  	   'key':key
			  }
	return params

def mkPoipara(address, key):
	params = {'version':'1', 
		  'count':'5',
		   'searchKeyword':address, 
		   'appKey':key
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

def mkTparaPth(stX, stY, edX, edY, passList, key):
	if passList == None:
		params = {'version':'1',
				  'startX':stX, 
				  'startY':stY,
				  'speed':'300',
				  'endX':edX, 
				  'endY':edY,
		   		  'startName':'%EC%B6%9C%EB%B0%9C',
		   		  'endName':'%EB%B3%B8%EC%82%AC',
		   		  'appKey':key
		  		 }
	else : 
		params = {'version':'1',
				  'startX':stX, 
				  'startY':stY,
				  'speed':'300',
				  'endX':edX, 
				  'endY':edY,
				  'passList':passList,
		   		  'startName':'%EC%B6%9C%EB%B0%9C',
		   		  'endName':'%EB%B3%B8%EC%82%AC',
		   		  'appKey':key
		  		 }
	return params
############################################33
def findElevation(listPath, url, key):
	lists = []
	
	for i in listPath:
		params = mkElepara(i[0], i[1], key)

		res = requests.get(url, params=params)
		lists.append(res.json()['results'][0]['elevation'])
	return lists

def findPthList(stX, stY, edX, edY ,psLst, url, key):
	lists = []
	
	pthParams = mkTparaPth(stX, stY, edX, edY, psLst, key)
	resPth = requests.post(url, data=pthParams)
	#pprint.PrettyPrinter(indent=4).pprint(resPth.json())
	for i in resPth.json()['features']:
		if type(i['geometry']['coordinates'][0]) == float :
			lists.append(i['geometry']['coordinates'])
			
	return lists


def findArnd(lstPth, lstEle, url, key):
	lon = listPath[listEle.index(max(listEle))][0]
	lat = listPath[listEle.index(max(listEle))][1]
	
	params = mkTparaArnd(lon, lat, key)
	
	res = requests.get(url, params=params)
	
	return res

def findArndEle(resArnd, url, key):
	listArndEle=[]
	listLocat=[]
	
	for i in resArnd.json()['searchPoiInfo']['pois']['poi']:
		params = mkElepara(i['frontLon'], i['frontLat'], key)
		res = requests.get(url, params=params)
		listArndEle.append(res.json()['results'][0]['elevation'])
		listLocat.append(res.json()['results'][0]['location'])
	
	return listArndEle, listLocat

def search(add, url, param):
	res = requests.get(url, params=param)
	number = 0
	for i in res.json()['searchPoiInfo']['pois']['poi']:
		print("%d. " %number, i['name'] )
		number+=1
		
	choose = input("번호를 선택해주세요 : ")
	return int(choose), res

def findPOI(url ,key):
	os.system("clear")
	addSt = input("출발지 : ")

	params = mkPoipara(addSt, key)
	chSt, resSt = search(addSt, url, params)

	stX = resSt.json()['searchPoiInfo']['pois']['poi'][chSt]['frontLon']
	stY = resSt.json()['searchPoiInfo']['pois']['poi'][chSt]['frontLat']

	os.system("clear")

	addEd = input("도착지 : ")

	params = mkPoipara(addEd, key)
	chEd, resEd = search(addSt, url, params)
	
	os.system("clear")

	edX = resEd.json()['searchPoiInfo']['pois']['poi'][chEd]['frontLon']
	edY = resEd.json()['searchPoiInfo']['pois']['poi'][chEd]['frontLat']
	return stX, stY, edX, edY

#basic setting
SKT=0
GOOGLE=1

pthUrl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
arndUrl = 'https://apis.openapi.sk.com/tmap/pois/search/around'
eleUrl = 'https://maps.googleapis.com/maps/api/elevation/json'
poiUrl = 'https://apis.openapi.sk.com/tmap/pois'

Tkey = mkKey(SKT)
Gkey = mkKey(GOOGLE)

listArndEle = []
listLocat = []

psLst = None
#start
stX, stY, edX, edY = findPOI(poiUrl ,Tkey)

#find path
listPath = findPthList(stX, stY, edX, edY ,psLst, pthUrl, Tkey)

#find path's elevation
listEle = findElevation(listPath, eleUrl, Gkey)

print("max :",max(listEle),"min :",min(listEle),"avr :",average(listEle))

#Around location about the highest elevation location
resArnd = findArnd(listPath, listEle, arndUrl, Tkey)

#find & save around location's elevation & lon & lat
listArndEle, listLocat=findArndEle(resArnd, eleUrl, Gkey)

psLst = str(listLocat[listArndEle.index(min(listArndEle))]['lng'])+","+ str(listLocat[listArndEle.index(min(listArndEle))]['lat'])

listPath = findPthList(stX, stY, edX, edY, psLst, pthUrl, Tkey)
###############################33
listEle = findElevation(listPath, eleUrl, Gkey)

print("max :",max(listEle),"min :",min(listEle),"avr :",average(listEle))


#add webopen

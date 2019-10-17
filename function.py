import requests
import json
import pprint
import time
import webbrowser
import os

def average(lists):
	return sum(lists) / len(lists)

def mkKey(site):
	if site == 0:
		key = open('/workspace/Python_test/final/Tmap/Test/txtFiles/tmapKey.txt', mode='rt', encoding='utf-8')

	if site == 1:
		key = open('/workspace/Python_test/final/Tmap/Test/txtFiles/gmapKey.txt', mode='rt', encoding='utf-8')
		
	return key.read()

def addPasslist(listLocat, listArndEle):
	return str(listLocat[listArndEle.index(min(listArndEle))]['lng'])+","+ str(listLocat[listArndEle.index(min(listArndEle))]['lat'])

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
		  'count':'20',
		 # 'categories':'편의점;한식;한의원',
		  'appKey':key
		  }
	return params

def mkTparaPth(lists, passList, key):
	if passList == None:
		params = {'version':'1',
				  'startX':lists[0], 
				  'startY':lists[1],
				  'speed':'300',
				  'endX':lists[2], 
				  'endY':lists[3],
		   		  'startName':'%EC%B6%9C%EB%B0%9C',
		   		  'endName':'%EB%B3%B8%EC%82%AC',
		   		  'appKey':key
		  		 }
	else : 
		params = {'version':'1',
				  'startX':lists[0], 
				  'startY':lists[1],
				  'speed':'300',
				  'endX':lists[2], 
				  'endY':lists[3],
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

def findPthList(drList ,psLst, url, key):
	lists = []
	
	pthParams = mkTparaPth(drList, psLst, key)
	resPth = requests.post(url, data=pthParams)
	
	for i in resPth.json()['features']:
		if type(i['geometry']['coordinates'][0]) == float :
			lists.append(i['geometry']['coordinates'])
			
	return lists


def findArnd(lstPth, lstEle, url, key):
	lon = lstPth[lstEle.index(max(lstEle))][0]
	lat = lstPth[lstEle.index(max(lstEle))][1]
	
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
		
	choose = input("Choose the number : ")
	return res.json()['searchPoiInfo']['pois']['poi'][int(choose)]

def findPOI(url ,key):
	os.system("clear")
	addSt = input("Start Point : ")

	params = mkPoipara(addSt, key)
	resSt = search(addSt, url, params)

	startName = resSt['name']
	stX = resSt['frontLon']
	stY = resSt['frontLat']

	os.system("clear")

	addEd = input("End Point : ")

	params = mkPoipara(addEd, key)
	resEd = search(addSt, url, params)
	
	os.system("clear")

	endName = resEd['name']
	edX = resEd['frontLon']
	edY = resEd['frontLat']
	
	print(f'start : {startName} -> end : {endName}\n')
	
	lists = [stX, stY, edX, edY]
	return lists

def noticePath(drList, passList, url, key):
	params=mkTparaPth(drList, passList, key)
	res = requests.post(url,data=params)

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
			
			
def openWeb(drList, passList, url, key):
	key = "appKey="+str(key)
	route = "startX="+str(drList[0])+"&startY="+str(drList[1])+"&endX="+str(drList[2])+"&endY="+str(drList[3])
	passlist = "passList="+str(passList)
	print(url+key+"&"+route+"&"+passlist)
	return key+"&"+route+"&"+passlist
	
def fastRoad(drList, url, key):
	psLst = None
	
	#notice path
	openWeb(drList, psLst, url['image'], key['tmap'])
	noticePath(drList, psLst, url['path'], key['tmap'])
	
def comforRoad(drList, url, key):
	psLst = None
	
	#find path & path's elevation
	listPath = findPthList(drList ,psLst, url['path'], key['tmap'])
	listEle = findElevation(listPath, url['ele'], key['gmap'])
	print("max :",max(listEle),"min :",min(listEle),"avr :",average(listEle))
	
	#find location & elevation around the highest location
	resArnd = findArnd(listPath, listEle, url['around'], key['tmap'])
	listArndEle, listLocat=findArndEle(resArnd, url['ele'], key['gmap'])
	
	psLst = addPasslist(listLocat, listArndEle)
	
	listPath = findPthList(drList ,psLst, url['path'], key['tmap'])
	listEle = findElevation(listPath, url['ele'], key['gmap'])
	print("max :",max(listEle),"min :",min(listEle),"avr :",average(listEle))
	
	openWeb(drList, psLst, url['image'], key['tmap'])
	noticePath(drList, psLst, url['path'], key['tmap'])
	
def menu():
	print("Choose Number")
	print("0. To find & notice fast road")
	print("1. To find & notice comfortable road")


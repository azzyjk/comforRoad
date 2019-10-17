from function import *

#basic setting
SKT=0
GOOGLE=1

url = {
		'path':'https://apis.openapi.sk.com/tmap/routes/pedestrian',
		'around':'https://apis.openapi.sk.com/tmap/pois/search/around',
		'ele':'https://maps.googleapis.com/maps/api/elevation/json',
		'poi':'https://apis.openapi.sk.com/tmap/pois',
		'image':'https://apis.openapi.sk.com/tmap/routeStaticMap?'
		}

key = {
		'tmap':mkKey(SKT),
		'gmap':mkKey(GOOGLE)
		}

#start
directList = findPOI(url['poi'], key['tmap'])

while(1):
	menu()
	choose = input()
	
	if(choose == '0'):
		os.system("clear")
		fastRoad(directList, url, key)
		break
	elif(choose=='1'):
		os.system("clear")
		comforRoad(directList, url, key)
		break
#add webopen

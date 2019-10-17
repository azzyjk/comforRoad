from function import *

#basic setting
SKT=0
GOOGLE=1

pthUrl = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
arndUrl = 'https://apis.openapi.sk.com/tmap/pois/search/around'
eleUrl = 'https://maps.googleapis.com/maps/api/elevation/json'
poiUrl = 'https://apis.openapi.sk.com/tmap/pois'
imageUrl = 'https://apis.openapi.sk.com/tmap/routeStaticMap?'

Tkey = mkKey(SKT)
Gkey = mkKey(GOOGLE)

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

psLst = addPasslist(listLocat, listArndEle)

listPath = findPthList(stX, stY, edX, edY, psLst, pthUrl, Tkey)

listEle = findElevation(listPath, eleUrl, Gkey)

print("max :",max(listEle),"min :",min(listEle),"avr :",average(listEle))

noticePath(stX, stY, edX, edY, psLst, pthUrl, Tkey)

openWeb(stX, stY, edX, edY, psLst, imageUrl, Tkey)
#add webopen

import requests
import pprint

url = 'https://apis.openapi.sk.com/tmap/routes/routeSequential30'
read = open('/workspace/Python_test/final/Tmap/Test/tmapKey.txt', mode='rt', encoding='utf-8')
key = read.read()

params = {
			'appKey':key,
			'version':'1', 
			'startTime':'201910101314',
			'startName':'%EC%B6%9C%EB%B0%9C', 
			'endName':'%EB%8F%84%EC%B0%A9',
			'startX': '126.956167', 
			'startY':'37.390458',
			'endX':'126.956971',
			'endY':'37.393164',
			'viaPoints':[
			  				{
								'viaPointid':'test',
								'viaPointName':'name', 
								'viaX':'126.95666686',
								'viaY':'37.3905020'
							}
						]
		  }

res = requests.post(url, data=params)

pprint.PrettyPrinter(indent=4).pprint(res.json())

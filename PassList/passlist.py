import requests
import pprint

url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
read = open('/workspace/Python_test/final/Tmap/Test/tmapKey.txt', mode='rt', encoding='utf-8')
key = read.read()

params = {
			'version':'1',
			'appKey':key,
			'startX': '126.956167', 
			'startY':'37.390458',
			'endX':'126.956971',
			'endY':'37.393164',
			'passList':'126.95666686, 37.3905020',
			'startName':'출발',
			'endName':'도착'
		}

res = requests.post(url, data=params)

pprint.PrettyPrinter(indent=4).pprint(res.json())
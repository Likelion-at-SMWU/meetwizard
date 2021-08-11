from meetwizard import settings
from shapely.geometry import Point
import requests
import json

def a(userPoint:Point, middlePoint:Point):
    time = 0   #소요시간

    #ODsay API 요청
    ODsay_url = f'https://api.odsay.com/v1/api/searchPubTransPathT?lang=0&SX={userPoint.x}&SY={userPoint.y}&EX={middlePoint.x}&EY={middlePoint.y}&OPT=0&apiKey={settings.ODSAY_KEY}'

    response = requests.get(ODsay_url).text
    return response
    response = json.loads(response)
    return response

    time += response['result']['path'][0]['info']['totalTime']
    return time
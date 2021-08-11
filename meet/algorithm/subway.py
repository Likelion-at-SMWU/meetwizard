import pandas as pd
import csv
import os
from shapely.geometry import Point
from accounts.models import User
from meet.models import Location

def find_nearby_subway(point:Point):
    subway = pd.read_csv('meetwizard/subway_info.csv', encoding='utf-8')

    subway_lat = list(subway['lat'])
    subway_lng = list(subway['lng'])
    subway_name = list(subway['name'])

    distance = 100
    j = 0

    for i in range(0,730): #730개의 역에 대해
        r = ((subway_lat[i]-point.y)**2+(subway_lng[i]-point.x)**2)**(1/2) #각 역의 위도와 경도를 뽑아내서 x,y좌표값 취급하여
        #사용자 위치의 위도(latitude)와 경도(longitude)와의 거리를 구함(r)
        if r <= distance: #그 거리 r이 최초에 정한 최소 거리(distance) 보다 작거나 같을 경우
            distance = r #최소 거리(distance)를 r(해당 역과 사용자 위치 간의 실제 거리)로 설정
            j = i #j는 어떤 번호를 가진 역이 가장 근거리에 있는지를 파악하기 위한 변수
            #r이 distance 보다 작거나 같을 경우에만 갱신되므로 큰 경우에 j는 증가하지 않고 distance와 r이 일치하는 마지막 역의 번호를 나타냄
    return subway_lat[j], subway_lng[j], subway_name[j]
    
    print("결과 거리값:", ((subway_lat[j]-point.y)**2+(subway_lng[j]-point.x)**2)**(1/2))
    print("결과 위치:", subway_lat[j], subway_lng[j])
    # j는 역 번호 -> 그래서 j라는 번호를 가진 역을 추출해야함 -> 그 역이 사용자 위치에서 가장 가까운 지하철역

    print("결과 지하철역:", subway_name[j])

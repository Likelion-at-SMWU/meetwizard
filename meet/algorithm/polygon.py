from typing import Sequence, Tuple
import math
from shapely.geometry import Point, Polygon
from meet.models import Location, Group, GroupMember, SelectedGroup

#다각형의 무게중심 구하기
def getCentroid(vertices: Sequence[Point]) -> Point:
    if (len(vertices) == 1):    #정점이 1개이면 그대로 반환
        return vertices[0]
    if (len(vertices) == 2):    #정점이 2개이면 평균 반환
        return Point((vertices[0].x + vertices[1].x)/2,(vertices[0].y + vertices[1].y)/2) 

    x_cent = y_cent = area = 0  #값 초기화
    v_local = vertices
    v_local.append(vertices[0])  #vertices의 0번째 요소 뒤에 붙이기 (0, 1, ..., n, 0)

    for i in range(len(v_local)-1):
        factor = v_local[i].x * v_local[i+1].y - v_local[i+1].x * v_local[i].y  #x[i]y[i+1] - x[i+1]y[i]
        area += factor
        x_cent += (v_local[i].x + v_local[i+1].x) * factor    #(x[i] + x[i+1]) * (x[i]y[i+1] - x[i+1]y[i])
        y_cent += (v_local[i].y + v_local[i+1].y) * factor    #(y[i] + y[i+1]) * (x[i]y[i+1] - x[i+1]y[i])

    area /= 2.0
    try: 
        x_cent /= (6 * area)
        y_cent /= (6 * area)
    except ZeroDivisionError:   #area=0일때 예외처리
        x_cent = -1
        y_cent = -1

    area = math.fabs(area)  #절대값으로 변환
    return Point(x_cent, y_cent)


#점이 다각형 내부에 들어있는지 체크하는 함수
def isInside(point: Point, vertices: Sequence[Point]): #parameter: 중간지점 Point, 다각형 Points
    return point.intersects(Polygon(vertices)) #다각형을 만들고 intersects() 함수를 통해 안에 들었는지 확인

# points를 줬을때 최대 거리 반환하도록 -> views에서 최대거리를 받아오도록. 
# 사용자위치와 무게중심 사이(centroidPoint / centroidPoint.x, centroidPoint.y) 의 거리 중 최대 거리
def get_map_level(points: Sequence[Point], centroidPoint:Point): #sequence: list, tuple 모두 포함
    distance = 0
    for i in range(len(points)):
        r = ((points[i].y-centroidPoint.y)**2+(points[i].x-centroidPoint.x)**2)**(1/2)
        if r >= distance:
            distance = r
            
    if 1.5 <= distance:
        level = 14
    elif 0.8 <= distance < 1.5:
        level = 13
    elif 0.6 <= distance < 0.8:
        level = 12
    elif 0.35 <= distance < 0.6:
        level = 11
    elif 0.18 <= distance < 0.35:
        level = 10
    elif 0.04 <= distance < 0.18:
        level = 9
    elif 0.01 <= distance < 0.04:
        level = 8
    else:
        level = 7

    return level
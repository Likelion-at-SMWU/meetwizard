from typing import Sequence
from shapely.geometry import Point
from random import randint
from math import atan2 

#그라함 알고리즘 함수
def graham_scan(points: Sequence[Point]):
    if (len(points) <= 2): return points   #point가 2개 이하이면 그라함 알고리즘 적용하지 않고 반환
    global anchor

    min_idx = None  #(y좌표, x좌표)로 정렬할 때 가장 작은 값의 인덱스
    for i, point in enumerate(points):
        if min_idx == None or point.y < points[min_idx].y:  #더 작은 y좌표를 가진 점으로 갱신
            min_idx = i
        elif point.y == points[min_idx].y and point.x < points[min_idx].x:  #y좌표가 같다면 더 작은 x좌표를 가진 점으로 갱신
            min_idx = i

    anchor = points[min_idx]

    sorted_pts = quicksort(points)  #polar angle를 기준으로 point 정렬
    del sorted_pts[sorted_pts.index(anchor)]    #anchor 삭제

    #hull 만들기
    hull = [anchor, sorted_pts[0]]  #앵커와 정렬 첫번째 요소로 다각형 초기화
    for s in sorted_pts[1:]:
        while det(hull[-2], hull[-1], s) <= 0:  #세 점이 같은 선상에있거나 시계방향으로 돈다면
            del hull[-1]    #backtrack(가장 최근에 추가된 요소 삭제)
        hull.append(s)  #while문이끝난 current point를 hull list에 추가
    
    return hull


#각을 기준으로 퀵정렬하는 함수
def quicksort(angle):
    if len(angle) <= 1: 
        return angle
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(angle[randint(0, len(angle) - 1)])    #polar angle 기준으로 중심점 찾기

    for pt in angle:
        pt_ang = polar_angle(pt)
        if pt_ang < piv_ang:    #pt의 각이 더 작다면 smaller에 pt를 추가
            smaller.append(pt) 
        elif pt_ang == piv_ang: #pt와 piv가 각이 같다면 equal에 pt를 추가
            equal.append(pt)
        else:   #pt의 각이 더 크다면 larger에 pt를 추가
            larger.append(pt)

    return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)


#p0에서 p1까지의 각을 계산하는 함수
def polar_angle(p0: Point, p1:Point=None):
    if p1 == None: p1 = anchor  #p1이 없다면 anchor로 대체
    y_span = p0.y - p1.y
    x_span = p0.x - p1.x
    return atan2(y_span, x_span)


#유클리드 거리를 구해주는 함수 (중간지점과 장소들 사이의 거리 계산)
def distance(p0:Point, p1:Point=None):
    if p1 == None: p1 = anchor  #p1이 없다면 anchor로 대체

    #x, y의 길이
    y_span = p0.y - p1.y    
    x_span = p0.x - p1.x

    return y_span**2 + x_span**2    #유클리드 거리 공식(제곱의 합)


#플라즈마 함수 (세 점이 반시계/시계/동일선상으로 도는 모습인지 판단)
# If > 0 - det 양이면 반시계방향으로 도는 모습
# If < 0 - det 음이면 시계방향으로 도는 모습
# If = 0 - det 0이면 세 점은 같은선상에있거나 직선에 있음
def det(p1,p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
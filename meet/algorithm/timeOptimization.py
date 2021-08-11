#최적 통행 비용을 가지지 않는 경우 이 함수를 돌림
from numpy import true_divide
from shapely.geometry import Point, Polygon
from typing import Sequence

from meet.algorithm import polygon

#새로운 중간지점을 도출하는 함수
def moveMiddlePoint(oldMiddle: Point, memberPoints: Sequence[Point]):
    x, y = 0, 0
    times = []

    for memberPoint in memberPoints:
        time = 0    #TODO:ODsay에서 얻은 소요시간
        times.append(time)  #소요시간을 리스트로 저장

        #벡터와 시간의 곱 (TODO:단위벡터가 아닌데 괜찮은가?)
        x += (memberPoint.x - oldMiddle.x) * time
        y += (memberPoint.y - oldMiddle.y) * time

    #사용자 수만큼 나눔
    x /= len(memberPoints)
    y /= len(memberPoints)
    
    #TODO: 벡터를 조절하기 위해 상수로 나눠야 함

    return Point(x, y), times

#최적 통행 비용인지 체크하는 함수
def isOptimizedResult(times:list[int], min_time_interval):    
    times.sort()    #소요시간 오름차순 정렬
    
    minTime = times[0]
    userCnt = 0

    for time in times:
        #첫번째 요소이거나 min_time_interval을 벗어나지 않는 경우는 넘어감
        if userCnt == 0 or time <= minTime + min_time_interval:
            userCnt += 1
        else:   #min_time_interval을 초과하는 경우 False 반환
            return False
    
    return True
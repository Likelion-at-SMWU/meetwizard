#최적 통행 비용을 가지지 않는 경우 이 함수를 돌림

#중간지점->사용자 노드 단위 벡터 구하기
#시간 가중치와 사용자의 단위 벡터 SUMPRODUCT
#노드 개수(!=인원수)와 상수로 나눔
#그라함 스캔으로 만든 다각형을 벗어났는지 체크(각의 합, 직선 긋기)

from shapely.geometry import Point, Polygon

#단위벡터 구하는 함수
def getUnitVector():    #parameter: (x1,y1), (x2,y2)
    return 0

#다각형 내부에 있는지 확인하는 함수 호출

#최적 통행 비용인지 체크하는 함수
#isOptimizedResult():    #parameter: (movingTimes, consideredUserCnt)
# max,min 차가 n개 이하이면 OK
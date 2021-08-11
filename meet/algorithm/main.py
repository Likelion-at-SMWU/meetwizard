from meet.models import GroupMember, Location, Schedule, Group
from accounts.models import User

from meet.algorithm import graham
from meet.algorithm import polygon
from meet.algorithm import timeOptimization
from meet.algorithm import subway
from meet.algorithm import scheduleOptimization

from shapely.geometry import Point

from dataclasses import dataclass

@dataclass(order=True)
class MemberSchedule:
    member: User
    day: str
    time: int
    value: float


#중간지점을 구하는 함수
def getMiddlePoint(group):
    memberPoints = createMemberPoints(group)    #쿼리셋을 Point 리스트 형식으로 변환
    if (len(memberPoints) == 1): return memberPoints[0]
    if (len(memberPoints) == 0): return Point(0,0)

    #그라함 알고리즘으로 외곽 점으로 이루어진 다각형 도출
    grahamPoints = graham.graham_scan(memberPoints)
    print("그라함 결과: ", grahamPoints)

    #무게중심을 통해 초기 중간지점 도출
    centroidPoint = polygon.getCentroid(grahamPoints)
    print("무게중심 결과: ", centroidPoint)   

    #중간지점과 가장 가까운 지하철역 찾기
    middlePoint = subway.find_nearby_subway(centroidPoint)
    print("가까운 지하철역 결과:", middlePoint)
    
    #ODsay API를 통해 각 사용자마다 소요시간 구하기
    #times=

    #최적의 중간지점인지 체크
    #timeOptimization.isOptimizedResult(times, 5)

    """
    #최적의 중간지점이 아니라면 다시 중간지점을 도출함
    while(not timeOptimization.isOptimizedResult(totalTimes, 5)):
        #아니라면, 다시 중간지점을 도출함(timeOptimization.moveMiddlePoint())
        middlePoint, totalTimes = timeOptimization.moveMiddlePoint(centroidPoint, memberPoints)

        #다각형 벗어났는지 체크
        print("다각형 내부 여부: ", polygon.isInside(middlePoint, grahamPoints))
    """


#스케줄을 취합하는 함수
def gatherSchedule(group):
    memberSchedules = createMemberSchedules(group)    #쿼리셋을 MemberSchedule 형식으로 변환
    result = scheduleOptimization.scheduleDivideIntoFour(memberSchedules, len(list(GroupMember.objects.filter(group=group))))

    #print(result)
    return result
    

#쿼리셋을 Point 리스트 형식으로 변환
def createMemberPoints(group):
    memberPoints = []
    members = GroupMember.objects.filter(group=group).values('member') #모델에서 선택한 그룹의 멤버 쿼리셋

    #쿼리셋에서 원하는 필드를 리스트로 저장
    longs = list(Location.objects.filter(user__in=members).values('longitude'))    #{'longitude', 값} 딕셔너리 형태의 리스트
    lats = list(Location.objects.filter(user__in=members).values('latitude'))  #{'latitude', 값} 딕셔너리 형태의 리스트

    #Point 데이터 클래스 형식으로 매칭하여 리스트에 추가
    for i in range(len(longs)): 
        memberPoints.append(Point(longs[i]['longitude'], lats[i]['latitude']))  #Point(x,y) 생성

    return memberPoints


#쿼리셋을 Schedule 리스트 형식으로 변환
def createMemberSchedules(group):
    memberSchedules = []
    members = GroupMember.objects.filter(group=group).values('member') #모델에서 선택한 그룹의 멤버 쿼리셋

    #쿼리셋에서 원하는 필드를 리스트로 저장
    users = list(Schedule.objects.filter(user__in=members).values('user'))  #{'user', 값} 딕셔너리 형태의 리스트
    days = list(Schedule.objects.filter(user__in=members).values('day'))    #{'day', 값} 딕셔너리 형태의 리스트
    times = list(Schedule.objects.filter(user__in=members).values('time'))  #{'time', 값} 딕셔너리 형태의 리스트
    values = list(Schedule.objects.filter(user__in=members).values('value'))  #{'value', 값} 딕셔너리 형태의 리스트

    #MemberSchedule 데이터 클래스 형식으로 매칭하여 리스트에 추가
    for i in range(len(users)): 
        memberSchedules.append(MemberSchedule(member=users[i]['user'], day=days[i]['day'], time=times[i]['time'], value=values[i]['value']))  #MemberSchedule 생성 및 리스트에 추가

    return memberSchedules


##
# 테스트를 위해 직접 실행
##
#getMiddlePoint(Group.objects.filter(name="만나조").first())
#gatherSchedule(Group.objects.filter(name="만나조").first())
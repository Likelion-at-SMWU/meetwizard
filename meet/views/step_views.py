from django.shortcuts import get_object_or_404, redirect, render, HttpResponsePermanentRedirect
from meet.models import Location, Schedule, Group, GroupMember, SelectedGroup
from accounts.models import User
from django.contrib.auth.decorators import login_required
from meet.algorithm.main import gatherSchedule, getMiddlePoint
from meet.algorithm import graham
from meet.algorithm import polygon
from meet.algorithm import main
from meet.algorithm import odsay    #TODO:나중에 지울것
from shapely.geometry import Point
"""
STEP 1
"""
@login_required
def meet_step1(request):
    global selected_group_gid
    param = {
        'leftType':3, 
        'groups':Group.objects.filter(host=request.user),
        'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
    }

    if ('group_name' in request.GET):  #그룹 조회 요청
        #GET으로 전달된 값 변수에 저장
        name = request.GET["group_name"]   #name: 조회하고 싶은 그룹 이름

        #모델 조회 및 param 변경
        groups = Group.objects.filter(host=request.user, name__contains=name)   #Group 조회
        param['groups'] = groups
        param['groups_members'] = GroupMember.objects.filter(group__in=groups)   #GroupMember 조회
        param['search_name'] = name
        
    if SelectedGroup.objects.filter(user=request.user):   
        param['gid'] = SelectedGroup.objects.filter(user=request.user).first().group.gid          #STEP1에서 선택된 그룹이 있음을 나타내기 위해 사용

    return render(request, 'meet/meet_step1.html', param)


#STEP1에서 선택한 그룹 gid 전역변수로 저장
@login_required
def saveGroupGid(request):
    global selected_group_gid
    if (request.method == "POST"):  
        gid = request.POST["selected_gid"]    
        group = Group.objects.filter(gid=gid).first()

        #SelectedGroup 모델에 업데이트
        updated_rows = SelectedGroup.objects.filter(user=request.user).update(group=group)

        #SelectedGroup 존재하지 않으면 추가
        if not updated_rows:    
            SelectedGroup.objects.create(user=request.user, group=group)

    return redirect('meet_step2')


#세부 그룹 정보 보여주기
@login_required
def meet_showall(request, gid):
    group = Group.objects.filter(host=request.user, gid=gid).first()

    #사용자가 볼 수 있는 그룹인지 체크
    if (not group):
        get_object_or_404(Group, pk=-1)

    param = {
        'leftType': 3, 
        'group': group,
        'group_members': GroupMember.objects.filter(group=group),
    }
    return render(request, 'meet/meet_showall.html', param)


"""
STEP 2
"""
@login_required
def meet_step2(request):
    param = {
        'leftType':3,  
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
    }

    return render(request, 'meet/meet_step2.html', param)


@login_required
def meet_step2_schedule_skipped(request):
    param = {
        'leftType':3,  
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
    }
    return render(request, 'meet/meet_step2_schedule_skipped.html', param)


@login_required
def meet_step2_location_skipped(request):
    param = {
        'leftType':3,
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
    }
    return render(request, 'meet/meet_step2_location_skipped.html', param)


"""
STEP 3
"""

@login_required
def meet_step3(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹

    param = {
        'leftType':3,  
        'group': selected_group,
    }

    #그룹 내 멤버들의 위치 취합
    members = GroupMember.objects.filter(group=selected_group).values('member')
    param['members_location'] = Location.objects.filter(user__in=members)

    #그라함으로 다각형 도출하고 무게중심 구하기
    #사용자 위치를 각 꼭짓점의 좌표로 받아서->그라함->무게중심
    #그 무게중심의 x값=경도, y값=위도로 대입(lat,lon)->그게 지도의 중심이 됨
    memberPoints = main.createMemberPoints(selected_group)
    grahamPoints = graham.graham_scan(memberPoints)
    centroidPoint = polygon.getCentroid(grahamPoints)
    param['latitude'] = centroidPoint.y     #지도의 중심점이 됨
    param['longitude'] = centroidPoint.x    #지도의 중심점이 됨

    #각 사용사간의 최장거리 구하기
    param['level'] = polygon.get_map_level(memberPoints, centroidPoint)
    
    #location의 정보가 없는 사용자 구하기
    no_data_members = members.difference(Location.objects.filter(user__in=members).values('user'))
    param['no_data_members'] = User.objects.filter(uid__in=no_data_members)

    #그룹 내 멤버들의 스케줄 취합
    param['members_schedules'] = gatherSchedule(selected_group)

    return render(request, 'meet/meet_step3.html', param)


@login_required
def meet_step3_schedule_skipped(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹

    param = {
        'leftType':3,
        'group': selected_group,  
    }

    #그룹 내 멤버들의 위치 취합
    members = GroupMember.objects.filter(group=selected_group).values('member')
    param['members_location'] = Location.objects.filter(user__in=members)
    
    #그라함으로 다각형 도출하고 무게중심 구하기
    #사용자 위치를 각 꼭짓점의 좌표로 받아서->그라함->무게중심
    #그 무게중심의 x값=경도, y값=위도로 대입(lat,lon)->그게 지도의 중심이 됨
    memberPoints = main.createMemberPoints(selected_group)
    grahamPoints = graham.graham_scan(memberPoints)
    centroidPoint = polygon.getCentroid(grahamPoints)
    param['latitude'] = centroidPoint.y     #지도의 중심점이 됨
    param['longitude'] = centroidPoint.x    #지도의 중심점이 됨

    #각 사용사간의 최장거리 구하기
    param['level'] = polygon.get_map_level(memberPoints, centroidPoint)
    
    #location의 정보가 없는 사용자 구하기
    no_data_members = members.difference(Location.objects.filter(user__in=members).values('user'))
    param['no_data_members'] = User.objects.filter(uid__in=no_data_members)


    return render(request, 'meet/meet_step3_schedule_skipped.html', param)


@login_required
def meet_step3_location_skipped(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹

    param = {
        'leftType':3,
        'group': selected_group,  
    }

    #그룹 내 멤버들의 스케줄 취합
    param['members_schedules'] = gatherSchedule(selected_group)
    return render(request, 'meet/meet_step3_location_skipped.html', param)


"""
STEP 4
"""
@login_required
def meet_step4(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹
    getMiddlePoint(selected_group)  #중간지점 도출

    param = {
        'leftType': 3,
    }

    #TODO: 그룹 내 멤버들의 스케줄, 위치 취합 (다른 py 작성 및 import해서 사용)
    #그룹 내 멤버들의 스케줄 취합
    param['members_schedules'] = gatherSchedule(selected_group)
    #param['schedules']=

    #TODO: 중간지점 도출 (다른 py 작성 및 import해서 사용)
    #param['result_point']=

    if (request.method == 'POST'):
        if 'food_btn' in request.POST:
            param['category'] = 1   #음식점 버튼 활성화

        elif 'cafe_btn' in request.POST:
            param['category'] = 2   #카페 버튼 활성화

        elif 'movie_btn' in request.POST:
            param['category'] = 3   #영화관 버튼 활성화

        elif 'parking_btn' in request.POST:
            param['category'] = 4   #주차장 버튼 활성화

        elif 'accomodation_btn' in request.POST:
            param['category'] = 5   #숙박 버튼 활성화

    return render(request, 'meet/meet_step4.html', param)


@login_required
def meet_step4_schedule_skipped(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹
    getMiddlePoint(selected_group)  #중간지점 도출
    
    param = {
        'leftType': 3,
    }

    #TODO: 그룹 내 멤버들의 위치 취합 (다른 py 작성 및 import해서 사용)
    #param['locations']=

    #TODO: 중간지점 도출 (다른 py 작성 및 import해서 사용)
    #param['result_point']=

    if (request.method == 'POST'):
        if 'food_btn' in request.POST:
            param['category'] = 1   #음식점 버튼 활성화

        elif 'cafe_btn' in request.POST:
            param['category'] = 2   #카페 버튼 활성화

        elif 'movie_btn' in request.POST:
            param['category'] = 3   #영화관 버튼 활성화

        elif 'parking_btn' in request.POST:
            param['category'] = 4   #주차장 버튼 활성화

        elif 'accomodation_btn' in request.POST:
            param['category'] = 5   #숙박 버튼 활성화

    return render(request, 'meet/meet_step4_schedule_skipped.html', param)


@login_required
def meet_step4_location_skipped(request):
    selected_group = SelectedGroup.objects.filter(user=request.user).first().group  #선택된 그룹

    param = {
        'leftType': 3,
    }

    #그룹 내 멤버들의 스케줄 취합
    param['members_schedules'] = gatherSchedule(selected_group)

    return render(request, 'meet/meet_step4_location_skipped.html', param)

def odsay_test(request):
    location = Location.objects.filter(user=request.user).first()
    userPoint = Point(location.longitude, location.latitude)
    """
    time = odsay.a(userPoint, Point(126.96462722521244, 37.54661108299542))
    param = {
        'leftType':2,   
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'error': time,
    }
    """
    return render(request, 'meet/test.html')

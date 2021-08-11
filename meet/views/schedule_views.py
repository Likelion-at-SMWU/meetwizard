from django.shortcuts import redirect, render, HttpResponsePermanentRedirect
from meet.models import Location, Schedule
from django.contrib.auth.decorators import login_required

"""
* choiceType: 스케줄 유형
    1: 약속 불가, 2: 약속 선호
* description: 스케줄 별칭
"""

@login_required
def schedule(request):
    param = {
            'leftType':2,  
            'location':Location.objects.filter(user=request.user).first(),
            'schedules':Schedule.objects.filter(user=request.user),
    }

    if request.method=='POST':
        if ('cant_meet' in request.POST):   #스케줄 유형 선택 request
            if (request.POST['cant_meet'] == "none" and request.POST['can_meet'] == "none"):    #어느 유형도 선택하지 않았을 경우
                param['error'] = "스케줄 유형을 선택하지 않았습니다."

            elif request.POST['cant_meet'] == "active":     #약속 불가 유형을 선택했을 경우
                param['choiceType'] = 1                             
                param['description'] = request.POST['description']  

            elif request.POST['can_meet'] == "active":      #약속 선호 유형을 선택했을 경우
                param['choiceType'] = 2                             
                param['description'] = request.POST['description']  

    return render(request, 'meet/schedule.html', param)


#'약속 불가' 스케줄 추가 요청
@login_required
def addDislikeSchedule(request):
    if request.method=='POST':
        #POST로 전달된 값 변수에 저장
        items = request.POST['red_changed'].split(',')
        items.remove("")                  #items: 스케줄 추가를 원하는 요일 및 시간들
        alias = request.POST['red_alias'] #alias: 스케줄 별칭

        #Schedule에 저장
        for item in items:
            day = item[0:3] #MON,TUE,WED,THU,FRI,SAT,SUN
            time = item[3:] #0900,0930,...

            #Schedule 모델에 업데이트
            updated_rows = Schedule.objects.filter(user=request.user, day=day, time=time).update(value=-1, alias=alias)

            #Schedule에 존재하지 않으면 추가
            if not updated_rows:    
                Schedule.objects.create(user=request.user, day=day, time=time, value=-1, alias=alias)

        return redirect('schedule')


#'약속 선호' 스케줄 추가 요청
@login_required
def addLikeSchedule(request):
    if request.method=='POST':
        #POST로 전달된 값 변수에 저장
        items = request.POST['green_changed'].split(',')
        items.remove("")                    #items: 스케줄 추가를 원하는 요일 및 시간들
        alias=request.POST['green_alias']   #alias: 스케줄 별칭

        #Schedule에 저장
        for item in items:
            day = item[0:3] #MON,TUE,WED,THU,FRI,SAT,SUN
            time = item[3:] #0900,0930,...

            #Schedule 모델에 업데이트
            updated_rows = Schedule.objects.filter(user=request.user, day=day, time=time).update(value=1, alias=alias)

            #Schedule에 존재하지 않으면 추가
            if not updated_rows:   
                Schedule.objects.create(user=request.user, day=day, time=time, value=1, alias=alias)

        return redirect('schedule')


#스케줄 삭제 요청
@login_required
def deleteSchedule(request):
    if request.method=='POST':
        #POST로 전달된 값 변수에 저장
        items = request.POST['empty_changed'].split(',')
        items.remove("")                    #items: 스케줄 삭제를 원하는 요일 및 시간들

        for item in items:
            day = item[0:3] #MON,TUE,WED,THU,FRI,SAT,SUN
            time = item[3:] #0900,0930,...

            #Schedule 모델에서 삭제
            Schedule.objects.filter(user=request.user, day=day, time=time).delete()

        return redirect('schedule')
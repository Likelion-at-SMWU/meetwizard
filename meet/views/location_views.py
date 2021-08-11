from django.shortcuts import redirect, render, HttpResponsePermanentRedirect
from meet.models import Location, Schedule
from django.contrib.auth.decorators import login_required

@login_required
def location(request):
    param = {
        'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
        'location':Location.objects.filter(user=request.user).first(),  #로케이션데이터중 (filter는 조건을 걸어주는명령어). 
        'schedules':Schedule.objects.filter(user=request.user),         #나request.user의데이터를가져온다
    }
    # Location.objects.filter(user=request.user).first().latitude (latitude나 longitude 하나 써주면 됨 -> 하나의 데이터 받아옴)
    # Schedule.objects.filter(user=request.user).values('latitude',...) -> 여러 데이터 가져올 수 있음
    return render(request, 'meet/location.html', param)


# 변경한 주소 저장 요청
@login_required
def saveLocation(request):
    if (request.method == 'POST'):
        #POST로 전달된 값 변수에 저장
        address = request.POST["address"]       #address: 주소
        latitude = request.POST["latitude"]     #latitude: 위도
        longitude = request.POST["longitude"]   #longitude: 경도

        #Location 모델에 업데이트
        updated_rows = Location.objects.filter(user=request.user).update(address=address, latitude=latitude, longitude=longitude)

        #Location 존재하지 않으면 추가
        if not updated_rows:    
            Location.objects.create(user=request.user, address=address, latitude=latitude, longitude=longitude)

        return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))
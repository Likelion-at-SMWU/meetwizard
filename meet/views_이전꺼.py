from django.shortcuts import redirect, render, HttpResponsePermanentRedirect
from .models import Location, Schedule, Friend, TemporaryFriend, Group, GroupMember
from accounts.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    param = {
        'leftType':0,   #왼쪽 고정창 없음
    }
    return render(request, 'meet/index.html', param)

def nonmemberhome(request):
    param = {
        'leftType':1,   #왼쪽 고정창에 비회원용 프로필, 위치, 스케줄 보여주기
    }
    return render(request, 'meet/nonmemberhome.html', param)

def home(request):
    if not request.user.is_authenticated:
        return redirect("nonmemberhome")

    param = {
        'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
    }
    return render(request, 'meet/home.html', param)

@login_required
def friendgroup(request):
    search_result = ""
    search_username = ""
    search_name = ""
    friend1 = Friend.objects.filter(user2=request.user)
    friend2 = Friend.objects.filter(user1=request.user)

    if request.method=="POST":
        if ('request_to_me_type' in request.POST):  #친구 수락/거절 폼
            send_uid = request.POST["send_uid"]
            send_user = User.objects.filter(uid=send_uid).first()
            receive_uid = request.POST["receive_uid"]
            receive_user = User.objects.filter(uid=receive_uid).first()

            TemporaryFriend.objects.filter(send_user = send_user, receive_user=receive_user).delete()   #TemporaryFriend에서 값 삭제
            if (request.POST["request_to_me_type"] == "1"):    #친구 수락이면 Friend 모델에 값 추가
                Friend.objects.create(user1=send_user, user2=receive_user)
            return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

        if ('group_name' in request.POST):   #그룹 추가 폼
            group_name = request.POST["group_name"]
            group_members = request.POST.getlist("group_member")
            #Group 모델에 값 추가
            group = Group.objects.create(name=group_name, host=request.user)
            #GroupMember 모델에 값 추가
            for member_uid in group_members:
                member = User.objects.filter(uid=member_uid).first()
                GroupMember.objects.create(group=group, member=member)
            GroupMember.objects.create(group=group, member=request.user)    #자신도 GroupMember에 추가
            return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

        if ('group_gid' in request.POST):   #그룹 삭제 폼
            group_gid = request.POST["group_gid"]
            group = Group.objects.filter(gid=group_gid).first()
            GroupMember.objects.filter(group=group).delete()
            group.delete()
            return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

        if ('friend_username' in request.POST): #username으로 사용자 검색 폼
            search_username = request.POST["friend_username"]
            search_result = User.objects.filter(username__contains=search_username)

        if ('uid_for_friend' in request.POST):  #친구요청
            uid = request.POST["uid_for_friend"]
            receive_user = User.objects.filter(uid=uid).first()
            TemporaryFriend.objects.create(send_user=request.user, receive_user=receive_user)
            return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

        if ('friend_name' in request.POST): #name으로 친구 검색 폼
            search_name = request.POST["friend_name"]
            friend1 = Friend.objects.filter(user1__in=User.objects.filter(name__contains=search_name) ,user2=request.user)
            friend2 = Friend.objects.filter(user1=request.user, user2__in=User.objects.filter(name__contains=search_name))

    param = {
        'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'groups':Group.objects.filter(host=request.user),
        'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
        'search_name':search_name,
        'friend1':friend1,
        'friend2':friend2,
        'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
        'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
        'search_username':search_username,
        'search_result':search_result,
    }
    return render(request, 'meet/friendgroup.html', param)

@login_required
def schedule(request):
    if request.method=='POST':
        if ('cant_meet' in request.POST):   #스케줄 유형 선택 request
            if (request.POST['cant_meet'] == "none" and request.POST['can_meet'] == "none"):    #어느 유형도 선택하지 않았을 경우
                param = {
                    'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
                    'location':Location.objects.filter(user=request.user).first(),
                    'schedules':Schedule.objects.filter(user=request.user),

                    'error': "스케줄 유형을 선택하지 않았습니다."   
                }
            elif request.POST['cant_meet'] == "active":
                param = {
                    'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
                    'location':Location.objects.filter(user=request.user).first(),
                    'schedules':Schedule.objects.filter(user=request.user),
                    'choiceType':1,   #약속 불가 선택
                    'description':request.POST['description'],
                }
            elif request.POST['can_meet'] == "active":
                param = {
                    'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
                    'location':Location.objects.filter(user=request.user).first(),
                    'schedules':Schedule.objects.filter(user=request.user),
                    'choiceType':2,   #약속 선호 선택
                    'description':request.POST['description'],
                }
        elif ('red_changed' in request.POST):   #스케줄 변경 request
            if (request.POST['red_changed'] != ""): #약속 불가 스케줄 추가
                items = request.POST['red_changed'].split(',')
                items.remove("")

                for item in items:
                    day = item[0:3]
                    time = item[3:]
                    #Schedule 모델에 업데이트
                    updated_rows = Schedule.objects.filter(user=request.user, day=day, time=time).update(value=-1, alias=request.POST['red_alias'])
                    if not updated_rows:    #모델에 존재하지 않으면 생성
                        Schedule.objects.create(user=request.user, day=day, time=time, value=-1, alias=request.POST['red_alias'])
                return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

            elif (request.POST['green_changed'] != ""): #약속 선호 스케줄 추가
                items = request.POST['green_changed'].split(',')
                items.remove("")

                for item in items:
                    day = item[0:3]
                    time = item[3:]
                    #Schedule 모델에 업데이트
                    updated_rows = Schedule.objects.filter(user=request.user, day=day, time=time).update(value=1, alias=request.POST['green_alias'])
                    if not updated_rows:    #모델에 존재하지 않으면 생성
                        Schedule.objects.create(user=request.user, day=day, time=time, value=1, alias=request.POST['green_alias'])
                return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

            elif (request.POST['empty_changed'] != ""):
                items = request.POST['empty_changed'].split(',')
                items.remove("")

                for item in items:
                    day = item[0:3]
                    time = item[3:]
                    #Schedule 모델에 삭제
                    updated_rows = Schedule.objects.filter(user=request.user, day=day, time=time).delete()
                return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

    else:        
        param = {
            'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
            'location':Location.objects.filter(user=request.user).first(),
            'schedules':Schedule.objects.filter(user=request.user),
        }
    return render(request, 'meet/schedule.html', param)

@login_required
def location(request):
    if (request.method == 'POST'):  #주소 "저장"을 요청할 경우
        address = request.POST["address"]
        latitude = request.POST["latitude"]
        longitude = request.POST["longitude"]

        #Location 모델에 업데이트
        updated_rows = Location.objects.filter(user=request.user).update(address=address, latitude=latitude, longitude=longitude)
        if not updated_rows:    #모델에 존재하지 않으면 생성
            Location.objects.create(user=request.user, address=address, latitude=latitude, longitude=longitude)
            
        param = {
            'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
            'location':Location.objects.filter(user=request.user).first(),
            'schedules':Schedule.objects.filter(user=request.user),
        }
        return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER', '/'))

    else:   #기본값이 없어서 예시데이터를 넣어줌
        param = {
            'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
            'location':Location.objects.filter(user=request.user).first(),
            'schedules':Schedule.objects.filter(user=request.user),
        }
    return render(request, 'meet/location.html', param)

@login_required
def meet_step1(request):
    groups = Group.objects.filter(host=request.user)
    groups_members = GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user))

    if (request.method == "POST"):  
        if ('group_name' in request.POST):
            name = request.POST["group_name"]
            groups = Group.objects.filter(host=request.user, name__contains=name)
            groups_members = GroupMember.objects.filter(group__in=groups)
        
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'groups':groups,
        'groups_members':groups_members,
    }
    return render(request, 'meet/meet_step1.html', param)

@login_required
def meet_step2(request):
    if (request.method == "POST"):  #STEP2로 넘어가기 위한 요청(선택한 gid 전달)
        if ('selected_gid' in request.POST):
            gid = request.POST["selected_gid"]
            group = Group.objects.filter(gid=gid).first()
            members = GroupMember.objects.filter(group=group)
            param = {
                'leftType':3,   #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'location':Location.objects.filter(user=request.user).first(),
                'schedules':Schedule.objects.filter(user=request.user),
                'gid':gid,  #STEP3까지 그룹 전달을 위해 gid만 전달
            }
            return render(request, 'meet/meet_step2.html', param)

    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'group': Group.objects.filter(host=request.user)[0],
    }
    return render(request, 'meet/meet_step2.html', param)

@login_required
def meet_step3(request):
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'address':"서울특별시 용산구 청파동2가 청파로 47길 100",    #나중에는 model에 있는 값으로 대체
        'latitude':37.546478390980596,
        'longitude':126.96486293693982,
    }
    return render(request, 'meet/meet_step3.html', param)

@login_required
def meet_step3_schedule_skipped(request):
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'address':"서울특별시 용산구 청파동2가 청파로 47길 100",    #나중에는 model에 있는 값으로 대체
        'latitude':37.546478390980596,
        'longitude':126.96486293693982,
    }
    return render(request, 'meet/meet_step3_schedule_skipped.html', param)

@login_required
def meet_step3_location_skipped(request):
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'address':"서울특별시 용산구 청파동2가 청파로 47길 100",    #나중에는 model에 있는 값으로 대체
        'latitude':37.546478390980596,
        'longitude':126.96486293693982,
    }
    return render(request, 'meet/meet_step3_location_skipped.html', param)

@login_required
def meet_step4(request):
    param = {
            'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        }
    if (request.method == 'POST'):
        if 'food_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 1, #음식점 버튼 활성화
            }
        elif 'cafe_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 2, #카페 버튼 활성화
            }
        elif 'movie_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 3, #영화관 버튼 활성화
            }
        elif 'parking_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 4, #주차장 버튼 활성화
            }
        elif 'accomodation_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 5, #숙박 버튼 활성화
            }
    return render(request, 'meet/meet_step4.html', param)

@login_required
def meet_step4_schedule_skipped(request):
    param = {
            'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        }
    if (request.method == 'POST'):
        if 'food_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 1, #음식점 버튼 활성화
            }
        elif 'cafe_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 2, #카페 버튼 활성화
            }
        elif 'movie_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 3, #영화관 버튼 활성화
            }
        elif 'parking_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 4, #주차장 버튼 활성화
            }
        elif 'accomodation_btn' in request.POST:
            param = {
                'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
                'category': 5, #숙박 버튼 활성화
            }
    return render(request, 'meet/meet_step4_schedule_skipped.html', param)

@login_required
def meet_step4_location_skipped(request):
    param = {
            'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
    }
    return render(request, 'meet/meet_step4_location_skipped.html', param)

@login_required
def meet_showall_1(request):
    param = {
        'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
    }
    return render(request, 'meet/meet_showall_1.html', param)

@login_required
def meet_showall_2(request):
    param = {
        'leftType': 3, #왼쪽 고정창에 사용자 프로필, STEP 보여주기
    }
    return render(request, 'meet/meet_showall_2.html', param)
    
@login_required
def meet_step2_schedule_skipped(request):
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'address':"서울특별시 용산구 청파동2가 청파로 47길 100",    #나중에는 model에 있는 값으로 대체
        'latitude':37.546478390980596,
        'longitude':126.96486293693982,
    }
    return render(request, 'meet/meet_step2_schedule_skipped.html', param)

@login_required
def meet_step2_location_skipped(request):
    param = {
        'leftType':3,  #왼쪽 고정창에 사용자 프로필, STEP 보여주기
        'address':"서울특별시 용산구 청파동2가 청파로 47길 100",    #나중에는 model에 있는 값으로 대체
        'latitude':37.546478390980596,
        'longitude':126.96486293693982,
    }
    return render(request, 'meet/meet_step2_location_skipped.html', param)

def meet_showall(request):
    return 0
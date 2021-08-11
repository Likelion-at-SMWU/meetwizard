from django.shortcuts import get_object_or_404, redirect, render, HttpResponsePermanentRedirect
from meet.models import Location, Schedule, Friend, TemporaryFriend, Group, GroupMember
from accounts.models import User
from django.contrib.auth.decorators import login_required

"""
* groups: 그룹
* groups_members: 각 그룹의 멤버
* friend: 친구
* request_to_friend: 내가 보낸 친구 요청
* request_to_me: 나에게 온 친구 요청
"""

@login_required
def friendgroup(request):
    #Friend 조회
    friend_uid = []
    friends1 = Friend.objects.filter(user2=request.user).values('user1')
    for friend in friends1:
        friend_uid.append(friend['user1'])
    friends2 = Friend.objects.filter(user1=request.user).values('user2')
    for friend in friends2:
        friend_uid.append(friend['user2'])

    #친구 중에서 자신을 제외한 User 조회
    friend = User.objects.filter(uid__in=friend_uid).order_by('name')

    param = {
        'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'groups':Group.objects.filter(host=request.user),
        'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
        'friend':friend,
        'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
        'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
    }
    return render(request, 'meet/friendgroup.html', param)


#그룹 추가 요청
@login_required
def createGroup(request):   
    if request.method=="POST": 
        #POST로 전달된 값 변수에 저장
        group_name = request.POST["group_name"]                 #group_name: 그룹명
        group_members = request.POST.getlist("group_member")    #group_members: 멤버(친구들 중 체크박스 true인 목록)

        if not Group.objects.filter(host=request.user, name=group_name):
            #Group에 추가
            group = Group.objects.create(name=group_name, host=request.user)

            #GroupMember에 추가
            for member_uid in group_members:
                member = User.objects.filter(uid=member_uid).first()
                GroupMember.objects.create(group=group, member=member)
            GroupMember.objects.create(group=group, member=request.user)    #자신도 GroupMember에 추가

            return redirect('friendgroup')
        else:
            #Friend 조회
            friend_uid = []
            friends1 = Friend.objects.filter(user2=request.user).values('user1')
            for friend in friends1:
                friend_uid.append(friend['user1'])
            friends2 = Friend.objects.filter(user1=request.user).values('user2')
            for friend in friends2:
                friend_uid.append(friend['user2'])

            #친구 중에서 자신을 제외한 User 조회
            friend = User.objects.filter(uid__in=friend_uid).order_by('name')

            param = {
                'leftType':2,  #왼쪽 고정창에 사용자 프로필, 위치, 스케줄 보여주기
                'location':Location.objects.filter(user=request.user).first(),
                'schedules':Schedule.objects.filter(user=request.user),
                'groups':Group.objects.filter(host=request.user),
                'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
                'friend':friend,
                'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
                'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
                'error':"이미 존재하는 그룹명입니다.",
            }
            return render(request, 'meet/friendgroup.html', param)


#그룹 삭제 요청
@login_required
def deleteGroup(request):   
    if request.method=="POST": 
        #POST로 전달된 값 변수에 저장
        group_gid = request.POST["group_gid"]   #group_gid: 삭제하고 싶은 그룹의 gid

        #Group 조회
        group = Group.objects.filter(gid=group_gid).first()

        #GroupMember에서 해당 멤버 삭제
        GroupMember.objects.filter(group=group).delete()

        #Group 삭제
        group.delete()

        return redirect('friendgroup')


#친구 수락 요청
@login_required
def acceptFriend(request):   
    if request.method=="POST":
        #POST로 전달된 값 변수에 저장
        send_uid = request.POST["send_uid"]         #send_uid: 친구 요청 보낸 사용자의 uid
        receive_uid = request.POST["receive_uid"]   #receive_uid: 친구 요청 대상의 uid

        #User 조회
        send_user = User.objects.filter(uid=send_uid).first()
        receive_user = User.objects.filter(uid=receive_uid).first()

        #TemporaryFriend에서 친구 요청 삭제
        TemporaryFriend.objects.filter(send_user=send_user, receive_user=receive_user).delete()   
        
        #Friend에 관계 추가
        if send_user.uid <= receive_user.uid:
            Friend.objects.create(user1=send_user, user2=receive_user)
        else:
            Friend.objects.create(user1=receive_user, user2=send_user)

        return redirect('friendgroup')


#친구 거절 요청
@login_required
def rejectFriend(request):   
    if request.method=="POST":
        #POST로 전달된 값 변수에 저장
        send_uid = request.POST["send_uid"]         #send_uid: 친구 요청 보낸 사용자의 uid
        receive_uid = request.POST["receive_uid"]   #receive_uid: 친구 요청 대상의 uid

        #User 조회
        send_user = User.objects.filter(uid=send_uid).first()
        receive_user = User.objects.filter(uid=receive_uid).first()

        #TemporaryFriend에서 친구 요청 삭제
        TemporaryFriend.objects.filter(send_user=send_user, receive_user=receive_user).delete()   

        return redirect('friendgroup')


#친구 요청
@login_required
def requestFriend(request):   
    #Friend 조회
    friend_uid = []
    friends1 = Friend.objects.filter(user2=request.user).values('user1')
    for friend in friends1:
        friend_uid.append(friend['user1'])
    friends2 = Friend.objects.filter(user1=request.user).values('user2')
    for friend in friends2:
        friend_uid.append(friend['user2'])

    #친구 중에서 자신을 제외한 User 조회
    friend = User.objects.filter(uid__in=friend_uid).order_by('name')

    param = {
        'leftType':2,
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'groups':Group.objects.filter(host=request.user),
        'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
        'friend':friend,
        'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
        'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
    }
    if request.method=="POST":  
        #POST로 전달된 값 변수에 저장
        uid = request.POST["uid_for_friend"]    #uid: 사용자가 친구 요청한 대상의 uid

        #User 조회
        receive_user = User.objects.filter(uid=uid).first()

        #친구 요청할 수 있는 상대인지 확인
        if ( 
            Friend.objects.filter(user1=receive_user, user2=request.user) or    #이미 친구인가?
            Friend.objects.filter(user1=request.user, user2=receive_user) or
            TemporaryFriend.objects.filter(send_user=request.user, receive_user=receive_user) or    #친구 요청을 이미 했는가?
            TemporaryFriend.objects.filter(send_user=receive_user, receive_user=request.user)
            ):  
            param['error'] = "이미 친구 요청했거나 친구입니다."
        
        else:
            #TemporaryFriend에 친구 요청 관계 추가
            TemporaryFriend.objects.create(send_user=request.user, receive_user=receive_user)   #send_user는 현재 로그인한 사용자

        return render(request, 'meet/friendgroup.html', param)


#친구 추가를 위한 사용자 검색(id)
@login_required
def searchUser(request):   
    if request.method=="GET": 
        #GET으로 전달된 값 변수에 저장
        search_username = request.GET["friend_username"]   #search_username: 조회하고 싶은 사용자 id
        
        #Friend 조회
        friend_uid = []
        friends1 = Friend.objects.filter(user2=request.user).values('user1')
        for friend in friends1:
            friend_uid.append(friend['user1'])
        friends2 = Friend.objects.filter(user1=request.user).values('user2')
        for friend in friends2:
            friend_uid.append(friend['user2'])

        #친구 중에서 자신을 제외한 User 조회
        friend = User.objects.filter(uid__in=friend_uid).order_by('name')

        #검색결과에서 친구인 상대와 자신을 제외한 User 조회
        search_result = User.objects.exclude(uid=request.user.uid).exclude(uid__in=friend_uid).filter(username__contains=search_username)
        search_result = search_result.order_by('username')

        param = {
            'leftType':2,
            'location':Location.objects.filter(user=request.user).first(),
            'schedules':Schedule.objects.filter(user=request.user),
            'groups':Group.objects.filter(host=request.user),
            'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
            'friend':friend,
            'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
            'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
            'search_username':search_username,  #검색에 사용한 keyword
            'search_result':search_result,      #검색 결과
        }

        return render(request, 'meet/friendgroup.html', param)


#친구 검색(name)
@login_required
def searchFriend(request):   
    if request.method=="GET": 
        #GET으로 전달된 값 변수에 저장
        search_name = request.GET["friend_name"]   #search_name: 조회하고 싶은 사용자 이름

        #Friend 조회
        friend_uid = []
        friends1 = Friend.objects.filter(user1__in=User.objects.filter(name__contains=search_name) ,user2=request.user).values('user1')
        for friend in friends1:
            friend_uid.append(friend['user1'])
        friends2 = Friend.objects.filter(user1=request.user, user2__in=User.objects.filter(name__contains=search_name)).values('user2')
        for friend in friends2:
            friend_uid.append(friend['user2'])

        #자신을 제외한 User 조회(친구 요청할 수 있는 상대인지 확인)
        friend = User.objects.filter(uid__in=friend_uid).order_by('name')

        param = {
                'leftType':2,
                'location':Location.objects.filter(user=request.user).first(),
                'schedules':Schedule.objects.filter(user=request.user),
                'groups':Group.objects.filter(host=request.user),
                'groups_members':GroupMember.objects.filter(group__in=Group.objects.filter(host=request.user)),
                'search_name':search_name,  #검색에 사용한 keyword
                'friend':friend,
                'request_to_friend':TemporaryFriend.objects.filter(send_user=request.user),
                'request_to_me':TemporaryFriend.objects.filter(receive_user=request.user),
        }

        return render(request, 'meet/friendgroup.html', param)


#그룹 자세히 보기
def group_showall(request, gid):
    group = Group.objects.filter(host=request.user, gid=gid).first()

    #사용자가 볼 수 있는 그룹인지 체크
    if (not group):
        get_object_or_404(Group, pk=-1)

    param = {
        'leftType': 2, 
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        'group': group,
        'group_members': GroupMember.objects.filter(group=group),
    }
    return render(request, 'meet/showall.html', param)
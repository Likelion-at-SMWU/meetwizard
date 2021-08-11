from django.urls import path
from .views import base_views, friendgroup_views, schedule_views, location_views, step_views

urlpatterns = [
    #base
    path('index/', base_views.index, name='index'),
    path('nonmemberhome/', base_views.nonmemberhome, name='nonmemberhome'),
    path('', base_views.home, name='home'),

    #friendgroup
    path('friendgroup/', friendgroup_views.friendgroup, name='friendgroup'),
    path('friendgroup/group/create', friendgroup_views.createGroup, name='createGroup'),
    path('friendgroup/group/delete', friendgroup_views.deleteGroup, name='deleteGroup'),
    path('friendgroup/friend/accept', friendgroup_views.acceptFriend, name='acceptFriend'),
    path('friendgroup/friend/delete', friendgroup_views.rejectFriend, name='rejectFriend'),
    path('friendgroup/friend/request', friendgroup_views.requestFriend, name='requestFriend'),
    path('friendgroup/user/search', friendgroup_views.searchUser, name='searchUser'),
    path('friendgroup/friend/search', friendgroup_views.searchFriend, name='searchFriend'),
    path('friendgroup/showall/<int:gid>', friendgroup_views.group_showall, name='group_showall'),

    #schedule
    path('schedule/', schedule_views.schedule, name='schedule'),
    path('schedule/dislike/add', schedule_views.addDislikeSchedule, name='addDislikeSchedule'),
    path('schedule/like/add', schedule_views.addLikeSchedule, name='addLikeSchedule'),
    path('schedule/delete', schedule_views.deleteSchedule, name='deleteSchedule'),

    #location
    path('location/', location_views.location, name='location'),
    path('location/save', location_views.saveLocation, name='saveLocation'),

    #step
    path('step1/', step_views.meet_step1, name='meet_step1'),
    path('step1/showall/<int:gid>', step_views.meet_showall, name='meet_showall'),
    path('step1/savegroup', step_views.saveGroupGid, name='saveGroupGid'),
    path('step2/', step_views.meet_step2, name='meet_step2'),
    path('step2/schedule_skipped/', step_views.meet_step2_schedule_skipped, name='meet_step2_schedule_skipped'),
    path('step2/location_skipped/', step_views.meet_step2_location_skipped, name='meet_step2_location_skipped'),
    path('step3/', step_views.meet_step3, name='meet_step3'),
    path('step3/schedule_skipped/', step_views.meet_step3_schedule_skipped, name='meet_step3_schedule_skipped'),
    path('step3/location_skipped/', step_views.meet_step3_location_skipped, name='meet_step3_location_skipped'),
    path('step4/', step_views.meet_step4, name='meet_step4'),
    path('step4/schedule_skipped/', step_views.meet_step4_schedule_skipped, name='meet_step4_schedule_skipped'),
    path('step4/location_skipped/', step_views.meet_step4_location_skipped, name='meet_step4_location_skipped'),

    path('test', step_views.odsay_test, name='odsay_test'),
]
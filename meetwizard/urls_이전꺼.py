from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import meet.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', meet.views.index, name='index'),
    path('nonmemberhome/', meet.views.nonmemberhome, name='nonmemberhome'),
    path('', meet.views.home, name='home'),
    path('friendgroup/', meet.views.friendgroup, name='friendgroup'),
    path('schedule/', meet.views.schedule, name='schedule'),
    path('location/', meet.views.location, name='location'),
    path('meet/step1/', meet.views.meet_step1, name='meet_step1'),
    path('meet/step2/', meet.views.meet_step2, name='meet_step2'),
    path('meet/step3/', meet.views.meet_step3, name='meet_step3'),
    path('meet/meet_step3_schedule_skipped/', meet.views.meet_step3_schedule_skipped, name='meet_step3_schedule_skipped'),
    path('meet/meet_step3_location_skipped/', meet.views.meet_step3_location_skipped, name='meet_step3_location_skipped'),
    path('meet/meet_step2_schedule_skipped/', meet.views.meet_step2_schedule_skipped, name='meet_step2_schedule_skipped'),
    path('meet/meet_step2_location_skipped/', meet.views.meet_step2_location_skipped, name='meet_step2_location_skipped'),
    path('meet/step4/', meet.views.meet_step4, name='meet_step4'),
    path('meet/meet_step4_schedule_skipped/', meet.views.meet_step4_schedule_skipped, name='meet_step4_schedule_skipped'),
    path('meet/meet_step4_location_skipped/', meet.views.meet_step4_location_skipped, name='meet_step4_location_skipped'),
    path('meet/showall1/', meet.views.meet_showall_1, name='meet_showall_1'),
    path('meet/showall2', meet.views.meet_showall_2, name='meet_showall_2'),
    path('meet/showall/<int:gid>', meet.views.meet_showall, name='meet_showall'),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
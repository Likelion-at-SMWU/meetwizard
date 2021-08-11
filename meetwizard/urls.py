from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import meet.views.base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', meet.views.base_views.home , name='home'),
    path('meet/', include('meet.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
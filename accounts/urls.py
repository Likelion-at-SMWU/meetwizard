from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# users/urls.py 오류나면 아래 두 줄에 해당되는 urlpatterns 지워 -혜준
#path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
#path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='accounts_delete'),
    path('password/', views.password, name='password'),
    path('update/', views.update, name='accounts_update'),
    path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),

    #비밀번호 재설정을 위한 url
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view()),

    # 비밀번호 찾기 url 오류나면 지워주세요 -다연
    path('recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),

] 
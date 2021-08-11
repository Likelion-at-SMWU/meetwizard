from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('setting/', views.setting, name='setting'),
    path('delete/', views.delete, name='accounts_delete'),
    path('password/', views.password, name='password'),
    path('update/', views.update, name='accounts_update'),

    #비밀번호 재설정을 위한 url
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view()),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
] 
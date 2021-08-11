from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserCreationForm
from .forms import CustomUserChangeForm
from django.contrib import auth
from meet.models import Friend
from accounts.models import User
from meet.models import Location, Schedule
from django.contrib.auth.views import PasswordResetView

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            #사용자가 테스트 해볼 수 있도록 test1, test2, test3, test4와 친구를 맺어줌
            # user = User.objects.filter(username=request.POST['username']).first()
            # test1 = User.objects.filter(username="test1").first()
            # test2 = User.objects.filter(username="test2").first()
            # test3 = User.objects.filter(username="test3").first()
            # test4 = User.objects.filter(username="test4").first()
    
            # Friend.objects.create(user1=user, user2=test1)
            # Friend.objects.create(user1=user, user2=test2)
            # Friend.objects.create(user1=user, user2=test3)
            # Friend.objects.create(user1=user, user2=test4)
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form, })

def login(request):
    if request.method == 'POST': #로그인 버튼 눌렀을 때
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None: #사용자 정보를 알맞게 입력
            auth.login(request, user)
            return redirect('home')
        else: #사용자 정보가 잘못 입력
            return render(request, 'accounts/login.html', {'error':'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('nonmemberhome')
    return render(request, 'accounts/signup.html')

@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'accounts/delete.html')

@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        
        # 키워드인자명을 함께 써줘도 가능
        # password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('login') 

        else:
            password_change_form = PasswordChangeForm(request.user)
            return render(request, 'accounts/password.html',{'error':'비밀번호 변경에 실패하였습니다.\n값을 정확히 입력했는지 확인해주세요.', 'password_change_form':password_change_form})
    
    else:
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html',{'password_change_form':password_change_form})

@login_required
def update(request):
    param = {
        'leftType':2,   
        'location':Location.objects.filter(user=request.user).first(),
        'schedules':Schedule.objects.filter(user=request.user),
        }
    if request.method == 'POST':
        if password_change_form.is_valid():
            user_change_form = CustomUserChangeForm(request.user, request.POST)
            user = user_change_form.save()
            return redirect('accounts_update')
        else:
            user_change_form = CustomUserChangeForm(instance = request.user)
            return render(request, 'accounts/update.html', {'error':'개인정보 수정에 실패하였습니다. \n값을 정확히 입력했는지 확인해주세요.', 'user_change_form':user_change_form})

    else:
        user_change_form = CustomUserChangeForm(instance = request.user)
        return render(request, 'accounts/update.html', {'user_change_form':user_change_form})


class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')
from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField #추가

from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import User #추가

#추가된 부분
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='비밀번호', 
        widget=forms.PasswordInput(attrs={
            'class':"form-control",
        })
    )
    password2 = forms.CharField(
        label='비밀번호 확인', 
        widget=forms.PasswordInput(attrs={
            'class':"form-control",
        })
    )

    class Meta:
        model = User
        fields = ('username','email', 'name', 'date_of_birth','tel','image')
        widgets = {
            'username':TextInput(attrs={
                'id': 'username',
                'class': "form-control",    #여기서 해당 input 태그의 class를 정해줄 수 있음
                'style': 'max-width: 200px;',   #여기서 style을 적을 수 있지만, CSS에서 클래스를 통해 적는 것을 추천
                'placeholder':'사용자 ID', 
            }),
            'email':EmailInput(attrs={
                'id': 'email',
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': '이메일 형식으로 입력하세요.',
            }),
            'name':TextInput(attrs={
                'id': 'name',
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder':'사용자 이름',
            }),
            'date_of_birth':forms.DateTimeInput(attrs={
                'id': 'date_of_birth',
                'class': 'form-control',
                'placeholder' : '\'yyyy-mm-dd\' 형식으로 입력하세요',
            }),
            'tel':NumberInput(attrs={
                'id': 'tel',
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': "'-'없이 입력하세요.'",
            }),
            'image':FileInput(attrs={
                # 'onchange': 'setThumbnail(event);',
            })
        }

    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 =self.cleaned_data.get("password2")
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField() #암호 수정불가

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'name', 'image', 'date_of_birth', 'email', 'tel', 'is_active', 'is_admin' )
        
#     def clean_password(self):
#         return self.initial["password"]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['image', 'date_of_birth', 'email', 'tel']
    # def clean_password(self):
    #   return self.initial["password"]

# users/forms.py 오류나면 아래 다 지워 -혜준

class RecoveryIdForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput,)
    email = forms.EmailField(widget=forms.EmailInput,)

    class Meta:
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_email' 
        })


# 비밀번호 찾기 forms.py 오류나면 그냥 싹 주석처리 해줘 -다연 
class RecoveryPwForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput,)
    name = forms.CharField(
        widget=forms.TextInput,)
    email = forms.EmailField(
        widget=forms.EmailInput,)

    class Meta:
        fields = ['username', 'name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_id',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })

# 비밀번호 찾기 후 새 비밀번호 입력 => 오류나면 주석처리 -다연
from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
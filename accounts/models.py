from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self, username, email, name, date_of_birth, tel, image, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            name = name,
            date_of_birth=date_of_birth,
            tel = tel,
            image = image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, date_of_birth, tel, image, password):
        user = self.create_user(
            username,
            email=email,
            password=password,
            name=name,
            date_of_birth=date_of_birth,
            tel=tel,
            image=image,
        )
        user.is_admin = True 
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(verbose_name='email', max_length=255)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    tel = models.CharField(max_length=11)
    image = models.ImageField(upload_to="accounts/%Y/%m/%d", blank=True, null=True)
    is_active = models.BooleanField(default=True)   #장고의 유저모델의 필수 필드
    is_admin = models.BooleanField(default=False)   #장고의 유저모델의 필수 필드

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'date_of_birth', 'tel', 'image']


    # 커스텀 유저 모델을 기본 유저 모델로 사용하기 위한 부분
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    
    
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

# Create your models here.
class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username

class Schedule(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=4)
    time = models.CharField(max_length=5)
    value = models.IntegerField(
        validators=[MinValueValidator(-1), MaxValueValidator(1)],
        default=0
    )
    alias = models.CharField(max_length=100, null=True, blank=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['user','day','time']

    def __str__(self):
        return self.user.username + ": " + self.day + self.time

class Friend(models.Model):
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (("user1", "user2"),)

    def __str__(self):
        return self.user1.username + ", " + self.user2.username

class TemporaryFriend(models.Model):
    send_user = models.ForeignKey(User, related_name='send_user', on_delete=models.CASCADE)
    receive_user = models.ForeignKey(User, related_name='receive_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("send_user", "receive_user"),)

    def __str__(self):
        return self.send_user.username + "->" + self.receive_user.username

class Group(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "host"),)

    def __str__(self):
        return self.host.username + " - " + self.name

class GroupMember(models.Model):    
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)  

    class Meta:
        unique_together = (("group", "member"),)

    def __str__(self):
        return self.group.name + " > " + self.member.username

class SelectedGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "group"),)

    def __str__(self):
        return self.user.name + " > " + self.group.name

from django.contrib import admin
from .models import Location, Schedule, Friend, SelectedGroup, TemporaryFriend, Group, GroupMember

# Register your models here.
admin.site.register(Location)
admin.site.register(Schedule)
admin.site.register(Friend)
admin.site.register(TemporaryFriend)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(SelectedGroup)
# Generated by Django 3.2 on 2021-08-04 13:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meet', '0009_selectedgroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='selectedgroup',
            unique_together={('user', 'group')},
        ),
    ]
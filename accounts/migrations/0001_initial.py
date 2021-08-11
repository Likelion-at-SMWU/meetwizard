# Generated by Django 3.2.4 on 2021-07-23 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('tel', models.CharField(max_length=11)),
                ('image', models.ImageField(blank=True, null=True, upload_to='accounts/%Y/%m/%d')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
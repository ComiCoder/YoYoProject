# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YYAccountInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phoneNum', models.CharField(max_length=32, null=True, verbose_name=b'phone number')),
                ('password', models.CharField(max_length=128, null=True, verbose_name=b'password')),
                ('nickName', models.CharField(max_length=32, null=True, verbose_name=b'nick name')),
                ('smallIconURL', models.ImageField(null=True, upload_to=b'images/profile_icon/')),
                ('largeIconURL', models.ImageField(null=True, upload_to=b'images/profile_icon/')),
                ('gender', models.SmallIntegerField(default=3, choices=[(1, b'Male'), (2, b'Female'), (3, b'-')])),
                ('selfDesc', models.CharField(max_length=300, null=True)),
                ('address', models.CharField(max_length=128, null=True)),
                ('zipcode', models.CharField(max_length=32, null=True)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('type', models.SmallIntegerField(default=1, choices=[(1, b'Normal'), (2, b'Admin')])),
                ('regProvince', models.SmallIntegerField(null=True)),
                ('regCity', models.SmallIntegerField(null=True)),
                ('authValue', models.SmallIntegerField(default=0)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

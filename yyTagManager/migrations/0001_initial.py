# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YYTagInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagType', models.IntegerField(default=1, choices=[(1, b'normal'), (2, b'overtime')])),
                ('tagValue', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updateTime', models.DateTimeField(auto_now=True, null=True)),
                ('validTime', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

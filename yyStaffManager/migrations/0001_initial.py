# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0001_initial'),
        ('yyImgManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YYStaffInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dealType', models.SmallIntegerField(default=1, choices=[(1, b'Trade'), (2, b'Present'), (3, b'Switch')])),
                ('staffDesc', models.CharField(max_length=300, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('position', models.CharField(default=b'-', max_length=100)),
                ('longitute', models.FloatField(default=0.0, null=True)),
                ('lagituite', models.FloatField(default=0.0, null=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updateTime', models.DateTimeField(auto_now=True, null=True)),
                ('albumInfo', models.ForeignKey(to='yyImgManager.YYAlbumInfo', null=True)),
                ('publisher', models.ForeignKey(to='yyUserCenter.YYAccountInfo', null=True)),
            ],
            options={
                'db_table': 'yy_staff_info',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YYFriendShipInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updateTime', models.DateTimeField(auto_now=True, null=True)),
                ('fromUser', models.ForeignKey(related_name='fromUserID', to='yyUserCenter.YYAccountInfo')),
                ('toUser', models.ForeignKey(related_name='toUserID', to='yyUserCenter.YYAccountInfo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

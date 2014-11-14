# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0001_initial'),
        ('yyStaffManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YYPostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updateTime', models.DateTimeField(auto_now=True, null=True)),
                ('postStaff', models.ForeignKey(to='yyStaffManager.YYStaffInfo')),
                ('postUser', models.ForeignKey(to='yyUserCenter.YYAccountInfo')),
            ],
            options={
                'db_table': 'yy_post_info',
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='yystaffinfo',
            old_name='lagituite',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='yystaffinfo',
            old_name='longitute',
            new_name='longitude',
        ),
    ]

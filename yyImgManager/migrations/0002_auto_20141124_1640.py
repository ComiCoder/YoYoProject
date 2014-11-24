# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyImgManager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yyimageinfo',
            name='height',
        ),
        migrations.RemoveField(
            model_name='yyimageinfo',
            name='imgURL',
        ),
        migrations.RemoveField(
            model_name='yyimageinfo',
            name='width',
        ),
        migrations.AddField(
            model_name='yyimageinfo',
            name='imgID',
            field=models.CharField(default=b'-', max_length=30),
            preserve_default=True,
        ),
    ]

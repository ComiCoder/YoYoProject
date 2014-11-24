# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yyaccountinfo',
            name='largeIconURL',
        ),
        migrations.RemoveField(
            model_name='yyaccountinfo',
            name='smallIconURL',
        ),
        migrations.AddField(
            model_name='yyaccountinfo',
            name='iconID',
            field=models.CharField(max_length=30, null=True),
            preserve_default=True,
        ),
    ]

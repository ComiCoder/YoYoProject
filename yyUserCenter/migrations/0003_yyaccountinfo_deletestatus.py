# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0002_auto_20141124_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='yyaccountinfo',
            name='deleteStatus',
            field=models.SmallIntegerField(default=0, choices=[(0, b'default'), (1, b'delete')]),
            preserve_default=True,
        ),
    ]

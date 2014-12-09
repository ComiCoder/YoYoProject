# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyTagManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='yytaginfo',
            table='yy_tag_info',
        ),
    ]

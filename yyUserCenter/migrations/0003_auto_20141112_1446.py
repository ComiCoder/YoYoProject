# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yyUserCenter', '0002_auto_20141112_1445'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='yyaccountinfo',
            table='yy_account_info',
        ),
    ]

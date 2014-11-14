# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YYAlbum2Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isPrimary', models.BooleanField(default=b'False')),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'yy_album_2_image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YYAlbumInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.CharField(default=b'', max_length=300)),
                ('status', models.SmallIntegerField(default=1, choices=[(0, b'delete'), (1, b'default')])),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'yy_album_info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YYImageInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imgURL', models.ImageField(upload_to=b'images/normalImgs/')),
                ('width', models.SmallIntegerField()),
                ('height', models.SmallIntegerField()),
                ('type', models.SmallIntegerField(default=1, choices=[(1, b'Staff'), (2, b'Activity')])),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'yy_image_info',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='yyalbuminfo',
            name='images',
            field=models.ManyToManyField(to='yyImgManager.YYImageInfo', through='yyImgManager.YYAlbum2Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='yyalbum2image',
            name='ImageInfo',
            field=models.ForeignKey(to='yyImgManager.YYImageInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='yyalbum2image',
            name='albumInfo',
            field=models.ForeignKey(to='yyImgManager.YYAlbumInfo'),
            preserve_default=True,
        ),
    ]

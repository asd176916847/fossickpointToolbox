# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-19 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0004_content_group_usercontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('doc', 'doc'), ('pdf', 'pdf'), ('image', 'image'), ('vedio', 'vedio'), ('audio', 'audio'), ('other', 'other')], max_length=30),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]

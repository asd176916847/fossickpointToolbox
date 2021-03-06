# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0011_auto_20170905_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileName', models.TextField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='content',
            name='profile',
        ),
        migrations.AddField(
            model_name='content',
            name='profile',
            field=models.ManyToManyField(to='toolbox.Profile'),
        ),
    ]

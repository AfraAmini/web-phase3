# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]

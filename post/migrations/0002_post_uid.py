# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-11 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='uid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-06 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='show_status',
            field=models.BooleanField(choices=[(True, '显示'), (False, '不显示')], default=False),
        ),
    ]

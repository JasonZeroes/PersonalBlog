# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-11 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsmodel',
            name='parent',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='comments.CommentsModel', verbose_name='评论的id'),
        ),
    ]
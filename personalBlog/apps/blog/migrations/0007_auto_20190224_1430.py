# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-24 14:30
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogarticle_blog_brief'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticle',
            name='blog_count',
            field=models.IntegerField(default=0, verbose_name='博客阅读量'),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='blog_brief',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=250, verbose_name='博客摘要'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 15:06
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshopper', '0011_auto_20171228_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us',
            name='message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='email_template',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=ckeditor.fields.RichTextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user_order',
            name='message',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]

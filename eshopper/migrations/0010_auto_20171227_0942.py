# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-27 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopper', '0009_user_order_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_order',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]

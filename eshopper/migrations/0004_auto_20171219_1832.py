# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopper', '0003_email_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us',
            name='contact_no',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]

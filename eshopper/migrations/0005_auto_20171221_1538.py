# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopper', '0004_auto_20171219_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_images',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
    ]
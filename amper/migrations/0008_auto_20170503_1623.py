# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-03 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amper', '0007_auto_20170503_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconfig',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='userconfig',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
    ]

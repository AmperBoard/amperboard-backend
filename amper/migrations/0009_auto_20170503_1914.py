# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-03 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amper', '0008_auto_20170503_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconfig',
            name='latitude',
            field=models.DecimalField(decimal_places=18, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='userconfig',
            name='longitude',
            field=models.DecimalField(decimal_places=18, max_digits=20, null=True),
        ),
    ]

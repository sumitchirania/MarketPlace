# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crud', '0002_auto_20160926_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='contact_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

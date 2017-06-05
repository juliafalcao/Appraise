# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0003_auto_20170602_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='activated',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Activated?'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='completed',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Completed?'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='retired',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Retired?'),
        ),
        migrations.AlterField(
            model_name='campaigndata',
            name='activated',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Activated?'),
        ),
        migrations.AlterField(
            model_name='campaigndata',
            name='completed',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Completed?'),
        ),
        migrations.AlterField(
            model_name='campaigndata',
            name='retired',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Retired?'),
        ),
        migrations.AlterField(
            model_name='campaignteam',
            name='activated',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Activated?'),
        ),
        migrations.AlterField(
            model_name='campaignteam',
            name='completed',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Completed?'),
        ),
        migrations.AlterField(
            model_name='campaignteam',
            name='retired',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Retired?'),
        ),
    ]

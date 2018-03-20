# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0004_auto_20180315_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='trajet',
            name='marque_voiture',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

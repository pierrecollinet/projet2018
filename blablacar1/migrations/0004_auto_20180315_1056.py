# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0003_auto_20180315_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='trajet',
            name='date_depart',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='heure_depart',
            field=models.TimeField(null=True, blank=True),
        ),
    ]

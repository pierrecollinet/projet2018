# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0009_ville'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajet',
            name='ville_arrivee',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='ville_depart',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

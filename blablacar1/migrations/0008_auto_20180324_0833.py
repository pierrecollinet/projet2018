# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0007_ratingconducteur'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='nom',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='prenom',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

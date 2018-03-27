# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0010_auto_20180326_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajet',
            name='ville_arrivee',
            field=models.ForeignKey(related_name='ville_arrivee', blank=True, to='blablacar1.Ville', null=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='ville_depart',
            field=models.ForeignKey(related_name='ville_depart', blank=True, to='blablacar1.Ville', null=True),
        ),
    ]

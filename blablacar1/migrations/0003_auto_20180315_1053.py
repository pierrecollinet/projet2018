# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0002_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heure_depart', models.DateTimeField()),
                ('ville_depart', models.CharField(max_length=100)),
                ('ville_arrivee', models.CharField(max_length=100)),
                ('capacite', models.PositiveSmallIntegerField()),
                ('prix_par_personne', models.CharField(max_length=100)),
                ('conducteur', models.ForeignKey(to='blablacar1.Utilisateur')),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]

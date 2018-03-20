# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0006_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingConducteur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proprete', models.CharField(max_length=100)),
                ('ponctualite', models.CharField(max_length=100)),
                ('commentaire', models.TextField()),
                ('auteur', models.ForeignKey(to='blablacar1.Utilisateur')),
                ('trajet', models.ForeignKey(to='blablacar1.Trajet')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0005_trajet_marque_voiture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('passager', models.ForeignKey(to='blablacar1.Utilisateur')),
                ('trajet', models.ForeignKey(to='blablacar1.Trajet')),
            ],
        ),
    ]

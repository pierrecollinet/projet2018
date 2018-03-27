# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0008_auto_20180324_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('code_postal', models.CharField(max_length=100)),
            ],
        ),
    ]

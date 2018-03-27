# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablacar1', '0012_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]

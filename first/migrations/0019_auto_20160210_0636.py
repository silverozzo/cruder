# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0018_auto_20160209_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'permissions': (('view_team', 'Can view team'),)},
        ),
        migrations.AlterModelOptions(
            name='teammate',
            options={'permissions': (('view_teammate', 'Can view teammates'),)},
        ),
    ]

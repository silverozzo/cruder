# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0008_team_teammate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'permissions': (('view_organization', 'can view details in admin'),)},
        ),
    ]

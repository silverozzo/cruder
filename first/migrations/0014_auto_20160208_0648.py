# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0013_auto_20160208_0618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'permissions': (('view_organization', 'Can view organization'),)},
        ),
    ]

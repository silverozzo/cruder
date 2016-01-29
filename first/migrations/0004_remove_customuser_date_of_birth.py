# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_auto_20160129_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_of_birth',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('first', '0014_auto_20160208_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission'),
        ),
    ]

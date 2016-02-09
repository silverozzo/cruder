# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0015_customuser_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', blank=True),
        ),
    ]

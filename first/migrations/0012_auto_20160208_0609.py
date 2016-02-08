# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0011_auto_20160205_1110'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Foobar',
        ),
        migrations.RemoveField(
            model_name='teammate',
            name='user',
        ),
        migrations.AddField(
            model_name='teammate',
            name='fullname',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]

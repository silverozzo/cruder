# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_auto_20160112_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foobar',
            name='extra_file',
            field=models.FileField(upload_to='uploads/', blank=True),
        ),
    ]

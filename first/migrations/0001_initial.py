# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foobar',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('content_text', models.CharField(max_length=200)),
                ('counter', models.IntegerField(default=0)),
                ('extra_file', models.FileField(upload_to='')),
            ],
        ),
    ]

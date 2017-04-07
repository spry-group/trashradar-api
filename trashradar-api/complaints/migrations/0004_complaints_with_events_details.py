# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0003_removing_events_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AddField(
            model_name='complaint',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='complaint',
            name='current_state',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='complaint',
            name='entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='complaints.Entity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='picture',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]

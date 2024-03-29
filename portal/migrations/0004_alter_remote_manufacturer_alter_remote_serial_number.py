# Generated by Django 5.0.1 on 2024-02-02 18:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_incident_call'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remote',
            name='manufacturer',
            field=models.CharField(default='SparkControl', max_length=100),
        ),
        migrations.AlterField(
            model_name='remote',
            name='serial_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]

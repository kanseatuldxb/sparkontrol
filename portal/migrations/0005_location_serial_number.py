# Generated by Django 5.0.1 on 2024-02-02 18:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_alter_remote_manufacturer_alter_remote_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='serial_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
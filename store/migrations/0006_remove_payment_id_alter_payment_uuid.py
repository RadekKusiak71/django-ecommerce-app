# Generated by Django 5.0.3 on 2024-04-04 17:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_payment_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='id',
        ),
        migrations.AlterField(
            model_name='payment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

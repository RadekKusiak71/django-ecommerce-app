# Generated by Django 5.0.3 on 2024-04-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_payment_id_alter_payment_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('paid', 'paid'), ('unpaid', 'unpaid')], default='unpaid', max_length=20),
        ),
    ]
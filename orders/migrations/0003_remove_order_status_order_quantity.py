# Generated by Django 4.2.17 on 2025-01-06 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_created_by_alter_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]

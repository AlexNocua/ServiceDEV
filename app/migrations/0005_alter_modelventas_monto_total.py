# Generated by Django 5.1.3 on 2024-11-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_modeldetalleventa_precio_unitario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelventas',
            name='monto_total',
            field=models.CharField(max_length=50),
        ),
    ]
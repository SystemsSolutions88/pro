# Generated by Django 5.1.5 on 2025-01-30 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competicion', '0003_resultado'),
    ]

    operations = [
        migrations.AddField(
            model_name='competidor',
            name='numero_corredor',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]

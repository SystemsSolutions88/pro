# Generated by Django 5.1.5 on 2025-02-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competicion', '0004_competidor_numero_corredor'),
    ]

    operations = [
        migrations.AddField(
            model_name='competidor',
            name='categoria',
            field=models.CharField(default='A', max_length=1),
        ),
    ]

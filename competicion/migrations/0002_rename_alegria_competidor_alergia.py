# Generated by Django 5.1.2 on 2024-10-17 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competicion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competidor',
            old_name='alegria',
            new_name='alergia',
        ),
    ]

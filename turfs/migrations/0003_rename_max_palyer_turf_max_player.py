# Generated by Django 4.1.7 on 2023-03-09 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turfs', '0002_turfimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turf',
            old_name='max_palyer',
            new_name='max_player',
        ),
    ]

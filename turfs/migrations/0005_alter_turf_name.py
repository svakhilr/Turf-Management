# Generated by Django 4.1.7 on 2023-03-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfs', '0004_timeslots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

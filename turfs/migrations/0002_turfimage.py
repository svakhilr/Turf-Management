# Generated by Django 4.1.7 on 2023-03-09 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turfs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurfImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turfimage', models.ImageField(upload_to='turfimages/')),
                ('turf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turf', to='turfs.turf')),
            ],
        ),
    ]
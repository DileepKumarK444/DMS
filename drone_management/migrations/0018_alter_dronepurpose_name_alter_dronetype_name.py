# Generated by Django 4.0.2 on 2022-09-06 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0017_dronetype_additional_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dronepurpose',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='dronetype',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

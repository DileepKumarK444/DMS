# Generated by Django 4.0.2 on 2022-09-06 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0018_alter_dronepurpose_name_alter_dronetype_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dronestatus',
            unique_together={('status', 'type')},
        ),
    ]

# Generated by Django 4.0.2 on 2022-09-06 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0020_alter_dronestatus_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dronestatus',
            unique_together={('status', 'type')},
        ),
    ]
# Generated by Django 4.0.2 on 2022-03-01 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0006_alter_drone_video_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drone',
            name='battery',
        ),
        migrations.RemoveField(
            model_name='drone',
            name='camera',
        ),
        migrations.RemoveField(
            model_name='drone',
            name='sensors',
        ),
    ]

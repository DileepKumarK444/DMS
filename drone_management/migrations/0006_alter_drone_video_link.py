# Generated by Django 4.0.2 on 2022-02-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0005_alter_drone_image_alter_drone_video_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='video_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
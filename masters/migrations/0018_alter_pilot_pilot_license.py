# Generated by Django 4.0.2 on 2022-03-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0017_alter_pilot_pilot_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='pilot_license',
            field=models.FileField(blank=True, null=True, upload_to='license_uploads/'),
        ),
    ]

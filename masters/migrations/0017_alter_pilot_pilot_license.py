# Generated by Django 4.0.2 on 2022-03-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0016_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='pilot_license',
            field=models.FileField(upload_to=''),
        ),
    ]

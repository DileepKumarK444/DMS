# Generated by Django 4.0.2 on 2022-03-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0012_alter_pilot_pilot_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='customer_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]

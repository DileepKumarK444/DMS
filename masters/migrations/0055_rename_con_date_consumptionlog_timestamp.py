# Generated by Django 4.0.2 on 2022-07-21 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0054_consumptionlog_con_date_consumptionlog_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumptionlog',
            old_name='con_date',
            new_name='timestamp',
        ),
    ]

# Generated by Django 4.0.2 on 2022-07-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0053_rename_vertual_memory_consumptionlog_virtual_memory'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumptionlog',
            name='con_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='consumptionlog',
            name='status',
            field=models.CharField(default='Unread', max_length=80, null=True),
        ),
    ]

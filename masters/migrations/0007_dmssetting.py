# Generated by Django 4.0.2 on 2022-02-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0006_customer_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DmsSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('conf_key', models.TextField()),
                ('conf_value', models.TextField()),
                ('conf_description', models.TextField()),
            ],
            options={
                'db_table': 'dms_settings',
            },
        ),
    ]

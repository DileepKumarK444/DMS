# Generated by Django 4.0.2 on 2022-03-17 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0027_rename_first_name_customer_account_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='description',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='customeruser',
            name='pilot_license',
            field=models.CharField(default='', max_length=80),
        ),
    ]

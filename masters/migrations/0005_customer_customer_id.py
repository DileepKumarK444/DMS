# Generated by Django 4.0.2 on 2022-02-25 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]
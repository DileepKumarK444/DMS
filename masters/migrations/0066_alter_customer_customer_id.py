# Generated by Django 4.0.2 on 2022-09-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0065_alter_country_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]
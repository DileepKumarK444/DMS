# Generated by Django 4.0.2 on 2022-02-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0005_customer_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='parent_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]

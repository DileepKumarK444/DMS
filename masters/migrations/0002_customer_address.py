# Generated by Django 4.0.2 on 2022-02-15 10:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

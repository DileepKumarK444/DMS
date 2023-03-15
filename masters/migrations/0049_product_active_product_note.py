# Generated by Django 4.0.2 on 2022-06-28 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0048_product_drone_status_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.0.2 on 2022-06-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0045_customeruser_additional_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='trans_type',
            field=models.CharField(choices=[('New', 'New'), ('Allocated', 'Allocated'), ('Danaged', 'Danaged')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='type',
            field=models.CharField(choices=[('Battery', 'Battery'), ('Sensor', 'Sensor'), ('Camera', 'Camera'), ('RC', 'RC')], default='Battery', max_length=80),
        ),
        migrations.AlterField(
            model_name='transactionlog',
            name='trans_type',
            field=models.CharField(choices=[('New', 'New'), ('Allocated', 'Allocated'), ('Danaged', 'Danaged')], default='New', max_length=10),
        ),
    ]

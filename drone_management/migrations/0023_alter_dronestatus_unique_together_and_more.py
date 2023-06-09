# Generated by Django 4.0.2 on 2022-09-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_management', '0022_alter_drone_model_no_alter_drone_serial_no_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dronestatus',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='drone',
            name='model_no',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='drone',
            name='serial_no',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='drone',
            name='uin',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dronepurpose',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dronetype',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

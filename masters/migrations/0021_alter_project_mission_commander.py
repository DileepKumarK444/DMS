# Generated by Django 4.0.2 on 2022-03-09 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0020_customeruser_pilot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='mission_commander',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.customeruser'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-04-12 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0037_dashboarddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboarddata',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.customer'),
        ),
    ]

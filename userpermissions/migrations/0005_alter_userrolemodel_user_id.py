# Generated by Django 4.0.2 on 2022-08-18 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userpermissions', '0004_alter_userrolemodel_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrolemodel',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

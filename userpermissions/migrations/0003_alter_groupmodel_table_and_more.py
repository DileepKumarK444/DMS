# Generated by Django 4.0.2 on 2022-02-15 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpermissions', '0002_auto_20201127_1207'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='groupmodel',
            table='dms_group',
        ),
        migrations.AlterModelTable(
            name='grouppermissionmodel',
            table='dms_group_permission',
        ),
        migrations.AlterModelTable(
            name='permissionmodel',
            table='dms_permission',
        ),
        migrations.AlterModelTable(
            name='rolegroupmodel',
            table='dms_role_group',
        ),
        migrations.AlterModelTable(
            name='rolemodel',
            table='dms_roles',
        ),
        migrations.AlterModelTable(
            name='userrolemodel',
            table='smd_user_roles',
        ),
    ]
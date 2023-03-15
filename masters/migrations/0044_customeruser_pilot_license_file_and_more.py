# Generated by Django 4.0.2 on 2022-05-03 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0043_alter_product_trans_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='pilot_license_file',
            field=models.FileField(blank=True, null=True, upload_to='license_uploads/'),
        ),
        migrations.AddField(
            model_name='customeruser',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='Profile_images/'),
        ),
    ]
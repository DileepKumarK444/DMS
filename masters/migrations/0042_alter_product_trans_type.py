# Generated by Django 4.0.2 on 2022-04-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0041_alter_category_additional_feature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='trans_type',
            field=models.CharField(default='new', max_length=10),
        ),
    ]

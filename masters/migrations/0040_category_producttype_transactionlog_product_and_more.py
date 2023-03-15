# Generated by Django 4.0.2 on 2022-04-26 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0039_plan_plan_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(default='', max_length=80)),
                ('additional_feature', models.CharField(default='', max_length=80)),
                ('warranty_period', models.IntegerField()),
                ('warranty', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dms_categories',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=80)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('battery', 'battery'), ('sensor', 'sensor'), ('camera', 'camera'), ('rc', 'rc')], default='battery', max_length=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dms_product_types',
            },
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trans_type', models.CharField(choices=[('new', 'new'), ('allocated', 'allocated'), ('Danaged', 'Danaged')], default='new', max_length=10)),
                ('quantity', models.IntegerField()),
                ('action', models.CharField(choices=[('add', 'add'), ('edit', 'edit'), ('delete', 'delete')], default='add', max_length=10)),
                ('date', models.DateField(null=True)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.category')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.producttype')),
            ],
            options={
                'db_table': 'dms_transaction_logs',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serial_number', models.CharField(default='', max_length=80)),
                ('trans_type', models.CharField(choices=[('new', 'new'), ('allocated', 'allocated'), ('Danaged', 'Danaged')], default='new', max_length=10)),
                ('pur_date', models.DateField(null=True)),
                ('warranty_start_date', models.DateField(null=True)),
                ('warranty_end_date', models.DateField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.category')),
            ],
            options={
                'db_table': 'dms_products',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.producttype'),
        ),
    ]

# Generated by Django 5.2.1 on 2025-06-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_paymentdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesDump',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('data', models.TextField()),
                ('created_at', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sales_dump',
                'managed': False,
            },
        ),
    ]

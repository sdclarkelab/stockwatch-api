# Generated by Django 3.0.7 on 2020-12-14 01:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('shares', models.IntegerField(default=0)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('gross_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('last_updated_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_action', to='transaction.TransactionAction')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_transaction', to='stock.Stock')),
            ],
        ),
    ]

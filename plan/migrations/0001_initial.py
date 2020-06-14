# Generated by Django 2.1.7 on 2020-01-19 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock_plan',
                                               to='stock.Stock')),
            ],
        ),
    ]

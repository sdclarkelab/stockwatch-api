# Generated by Django 3.0.7 on 2021-03-13 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('plan', '0002_remove_plan_sold_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='target_sell_price',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]

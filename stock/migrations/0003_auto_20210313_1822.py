# Generated by Django 3.0.7 on 2021-03-13 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stock', '0002_auto_20201213_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcalculateddetail',
            name='avg_net_price',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockcalculateddetail',
            name='current_value',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockcalculateddetail',
            name='total_net_amount',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockcalculateddetail',
            name='total_shares',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
    ]

# Generated by Django 3.0.7 on 2021-03-13 23:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stock', '0003_auto_20210313_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.TextField(max_length=50),
        ),
    ]

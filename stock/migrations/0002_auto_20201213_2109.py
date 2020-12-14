# Generated by Django 3.0.7 on 2020-12-14 02:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='name',
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last_updated_date',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

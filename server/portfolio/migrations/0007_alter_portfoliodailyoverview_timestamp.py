# Generated by Django 4.2.5 on 2024-03-08 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_rename_change_current_value_portfoliodailyoverview_change_invested_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliodailyoverview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 8, 14, 20, 53, 201886)),
        ),
    ]

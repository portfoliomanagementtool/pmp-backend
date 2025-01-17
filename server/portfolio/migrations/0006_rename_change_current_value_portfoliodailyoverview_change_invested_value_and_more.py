# Generated by Django 4.2.5 on 2024-03-08 07:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_portfoliodailyoverview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfoliodailyoverview',
            old_name='change_current_value',
            new_name='change_invested_value',
        ),
        migrations.RenameField(
            model_name='portfoliodailyoverview',
            old_name='change_total_investment',
            new_name='change_market_value',
        ),
        migrations.RenameField(
            model_name='portfoliodailyoverview',
            old_name='current_value',
            new_name='invested_value',
        ),
        migrations.RenameField(
            model_name='portfoliodailyoverview',
            old_name='day_pl',
            new_name='market_value',
        ),
        migrations.RenameField(
            model_name='portfoliodailyoverview',
            old_name='day_pl_percentage',
            new_name='overall_pl',
        ),
        migrations.RemoveField(
            model_name='portfoliodailyoverview',
            name='total_investment',
        ),
        migrations.AddField(
            model_name='portfoliodailyoverview',
            name='change_overall_pl',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfoliodailyoverview',
            name='percent_change_invested_value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfoliodailyoverview',
            name='percent_change_market_value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfoliodailyoverview',
            name='percent_change_overall_pl',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='portfoliodailyoverview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 8, 13, 28, 37, 196810)),
        ),
    ]

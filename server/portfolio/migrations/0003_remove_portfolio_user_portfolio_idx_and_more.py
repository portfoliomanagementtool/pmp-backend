# Generated by Django 4.2.5 on 2024-01-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_portfolio_transactionitem_delete_portfolioitem_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='portfolio',
            name='user_portfolio_idx',
        ),
        migrations.RenameField(
            model_name='portfolio',
            old_name='portfolio_asset_v1',
            new_name='portfolio_asset',
        ),
        migrations.AddIndex(
            model_name='portfolio',
            index=models.Index(models.F('user'), models.F('portfolio_asset'), name='user_portfolio_idx'),
        ),
    ]

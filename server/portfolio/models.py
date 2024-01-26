from django.db import models
from pmp_user.models import pmp_user
from assets.models import Asset
# Create your models here.
class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    pmp_user= models.ForeignKey(pmp_user, on_delete=models.CASCADE,related_name='watchlist_user')
    name = models.CharField(max_length=50)
    watchlist_assets=models.ManyToManyField(Asset,blank=True,related_name='watchlist_assets',name='watchlist_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "watchlists"

class TransactionItem(models.Model):
    user= models.ForeignKey(pmp_user, on_delete=models.CASCADE,related_name='transaction_user')
    transaction_asset=models.ForeignKey(Asset, on_delete=models.CASCADE,related_name='transaction_asset',name='transaction_asset')
    quantity=models.IntegerField()
    buy_price=models.FloatField(null=True,blank=True)
    sell_price=models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "transaction_items"


class Portfolio(models.Model):
    user= models.ForeignKey(pmp_user, on_delete=models.CASCADE,related_name='portfolio_user_v1')
    portfolio_asset=models.ForeignKey(Asset, on_delete=models.CASCADE,related_name='portfolio_asset_v1',name='portfolio_asset')
    quantity=models.FloatField()
    avg_buy_price=models.FloatField(null=True,blank=True)
    avg_sell_price=models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "portfolios" 
        indexes = [
            models.Index("user", "portfolio_asset", name="user_portfolio_idx")
        ]
from django.db import models
from assets.models import Asset
class asset_pricing(models.Model):
    ticker = models.ForeignKey(Asset, max_length=10,related_name="asset_price_relation",on_delete=models.CASCADE,default=None)
    market_value = models.FloatField("Market Value")
    open=models.FloatField(blank=True,null=True)
    close=models.FloatField(blank=True,null=True)
    high=models.FloatField(blank=True,null=True)
    low=models.FloatField(blank=True,null=True)
    ft_week_high=models.FloatField(blank=True,null=True)
    ft_week_low=models.FloatField(blank=True,null=True)
    month_high=models.FloatField(blank=True,null=True)
    month_low=models.FloatField(blank=True,null=True)
    overall_high=models.FloatField(blank=True,null=True)
    overall_low=models.FloatField(blank=True,null=True)
    
    timestamp1 = models.DateTimeField(auto_now=False, auto_now_add=False)
    currency = models.CharField("Enter Currency", max_length=10)

    class Meta:
        db_table = "asset_pricing1"
        unique_together = (('ticker', 'timestamp1'))

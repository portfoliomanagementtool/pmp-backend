from django.db import models

class asset_pricing(models.Model):
    ticket = models.CharField("Enter Ticker", max_length=10)
    market_traded = models.CharField("Market Traded", max_length=20)
    market_value = models.IntegerField("Market Value")
    timestamp1 = models.DateTimeField(auto_now=False, auto_now_add=False)
    currency = models.CharField("Enter Currency", max_length=10)

    class Meta:
        db_table = "asset_pricing1"
        unique_together = (('ticket', 'market_traded', 'timestamp1'))

from django.db import models

class asset_pricing(models.Model):
    ticker = models.CharField("Enter Ticker", max_length=10,primary_key=True)  
    market_traded = models.DecimalField("Market Traded", max_digits=5, decimal_places=5)  
    market_value = models.DecimalField("Market Value", max_digits=5, decimal_places=5) 
    timestamp1 = models.TimeField(auto_now=False, auto_now_add=False)  
    currency = models.CharField("Enter Currency", max_length=10,primary_key=False)
    
    class Meta:  
        db_table = "asset_pricing"
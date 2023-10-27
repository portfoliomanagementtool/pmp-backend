from django.db import models

class Asset(models.Model):
    ticker = models.CharField("Enter Ticker", max_length=10,primary_key=True)  
    category = models.CharField("Enter Category Name", max_length = 20)  
    name = models.CharField("Enter Name", max_length = 20) 
    description = models.CharField("Enter Description", max_length = 60)  
  
    class Meta:  
        db_table = "asset"
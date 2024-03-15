from rest_framework.serializers import ModelSerializer
from .models import Asset
from rest_framework.serializers import SerializerMethodField,JSONField
from asset_pricing.models import asset_pricing
# from asset_pricing.serializers import AssetPricingSerializer
class AssetSerializer(ModelSerializer):
    class Meta:
        model=Asset
        fields='__all__'


class AssetSerializerWithPricing(ModelSerializer):
    def getPricingDetails(self,asset):
        pricing=asset_pricing.objects.filter(ticker=asset.ticker).latest('timestamp1')
        
        if(pricing==None):
            return None
        return pricing.market_value
    
    def getDayPL(self,asset):
        pricing=asset_pricing.objects.filter(ticker=asset.ticker).latest('timestamp1')
        
        if(pricing==None):
            return 0
        return pricing.day_change

    pricing=SerializerMethodField('getPricingDetails')
    daypl=SerializerMethodField('getDayPL')
    class Meta:
        model=Asset
        fields=['ticker','category','name','pricing','daypl']
    def to_representation(self, instance):
        asset=super().to_representation(instance)
        if asset['pricing']==None:
            return asset
        if asset['pricing']==0:
            asset['daypl_percent']=0
        else:
            asset['daypl_percent']=asset['daypl']/asset['pricing']*100
        return asset
    


class BaseAssetPricing(ModelSerializer):
    
    class Meta:
        model=asset_pricing
        fields='__all__'
    
class AssetSerializerWithPricingForTableData(ModelSerializer):
    def getPricingDetails(self,asset):
        try:
            pricing=asset_pricing.objects.filter(ticker=asset.ticker).latest('timestamp1')
            print(pricing)
            if(pricing==None):
                return None
            return BaseAssetPricing(pricing,many=False).data
        except:
            return None
    
    pricing=SerializerMethodField('getPricingDetails')

    class Meta:
        model=Asset
        fields=['ticker','category','name','pricing']
    
    def to_representation(self, data):
        data = super(AssetSerializerWithPricingForTableData, self).to_representation(data)
        if(data['pricing']==None):
            return data
        data['high']=data['pricing']['high']
        data['open']=data['pricing']['open']
        data['low']=data['pricing']['low']
        data['close']=data['pricing']['close']
        data['day_change']=data['pricing']['day_change']
        data['day_change_percentage']=data['pricing']['day_change_percentage']
        data['highLow']={
            'today':{
                'high':data['pricing']['high'],
                'low':data['pricing']['low'],
            },
            '52week':{
                'high':data['pricing']['ft_week_high'],
                'low':data['pricing']['ft_week_low'],
            },
            'overall':{
                'high':data['pricing']['overall_high'],
                'low':data['pricing']['overall_low']
            }
        }
        data['market_value']=data['pricing']['market_value']
        data.pop('pricing')

        return data
    

class AssetSerializerWithPricingV2(ModelSerializer):
    def getPricingDetails(self,asset):
        pricing=asset_pricing.objects.filter(ticker=asset.ticker).latest('timestamp1')
        if(pricing==None):
            return None
        return pricing.market_value
    pricing=SerializerMethodField('getPricingDetails')
    class Meta:
        model=Asset
        fields=['ticker','category','name','price']


"""
    ticker = models.CharField("Enter Ticker", max_length=10,primary_key=True)  
    category = models.CharField("Enter Category Name", max_length = 20)  
    name = models.CharField("Enter Name", max_length = 20) 
    description = models.CharField("Enter Description", max_length = 60)  
  
"""
"""
category: "Technology",
      ticker: "AAPL",
      price: 150.5,
      avgBasis: 140.25,
      quantity: 100,
      marketValue: 15050.0,
      costBasis: 14025.0,
      profitLoss: 1025.0,
      percentPL: 7.32,
      portfolioPercent: 12.5,
      categoryPercent: 10.2,
"""
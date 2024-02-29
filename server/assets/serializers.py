from rest_framework.serializers import ModelSerializer
from .models import Asset
from rest_framework.serializers import SerializerMethodField,JSONField
from asset_pricing.models import asset_pricing

# from asset_pricing.serializers import BaseAssetPricing
class AssetSerializer(ModelSerializer):
    class Meta:
        model=Asset
        fields='__all__'


class AssetSerializerWithPricing(ModelSerializer):
    def getPricingDetails(self,asset):
        pricing=asset_pricing.objects.filter(ticker=asset.ticker).last()
        if(pricing==None):
            return None
        return {'price':pricing.market_value,'timestamp':pricing.timestamp1,'currency':pricing.currency}
    

    pricing=SerializerMethodField('getPricingDetails')

    class Meta:
        model=Asset
        fields=['ticker','category','name','pricing']
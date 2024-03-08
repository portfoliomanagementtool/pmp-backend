from rest_framework import serializers
from .models import asset_pricing
from assets.serializers import AssetSerializer

class AssetPricingSerializer(serializers.ModelSerializer):
    # ticket=AssetSerializer(many=False, read_only=True)
    class Meta:
        model = asset_pricing
        fields = '__all__'

class GainLossSerializer(serializers.ModelSerializer):
    ticker=AssetSerializer(many=False, read_only=True)
    
    class Meta:
        model = asset_pricing

        fields = "__all__"
    def to_representation(self, data):
        data = super(GainLossSerializer, self).to_representation(data)
        response={
            "ticker":data['ticker']["ticker"],
            "category":data["ticker"]["category"],
            "price":data['close'],
            "day_change_percentage":data['day_change_percentage'],
            "day_change":data['day_change'],
            "timestamp":data['timestamp1']
        }
        return response

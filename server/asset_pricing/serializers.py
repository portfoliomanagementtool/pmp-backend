from rest_framework import serializers
from .models import asset_pricing
from assets.serializers import AssetSerializer

class AssetPricingSerializer(serializers.ModelSerializer):
    ticket=AssetSerializer(many=False, read_only=True)
    class Meta:
        model = asset_pricing
        fields = '__all__'

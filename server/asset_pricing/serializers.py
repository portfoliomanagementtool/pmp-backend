from rest_framework import serializers
from .models import asset_pricing

class AssetPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = asset_pricing
        fields = '__all__'

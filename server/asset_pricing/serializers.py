from rest_framework.serializers import ModelSerializer
from .models import asset_pricing

class AssetPricingSerializer(ModelSerializer):
    class Meta:
        model=asset_pricing
        fields='__all__'
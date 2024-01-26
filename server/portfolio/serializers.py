from rest_framework import serializers
from .models import TransactionItem,Portfolio
from assets.serializers import AssetSerializer
class TransactionItemSerializer(serializers.ModelSerializer):
    transaction_asset=AssetSerializer(many=False, read_only=True)
    
    class Meta:
        model = TransactionItem
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    portfolio_asset=AssetSerializer(many=False, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
    
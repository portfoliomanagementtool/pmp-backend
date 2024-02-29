from rest_framework import serializers
from .models import TransactionItem,Portfolio,Watchlist
from assets.serializers import AssetSerializerWithPricing,AssetSerializer
from asset_pricing.serializers import AssetPricingSerializer
class TransactionItemSerializer(serializers.ModelSerializer):
    transaction_asset=AssetSerializer(many=False, read_only=True)
    
    class Meta:
        model = TransactionItem
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    portfolio_asset=AssetSerializerWithPricing(many=False, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
    

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id','pmp_user','name','created_at','updated_at']



class WatchlistWithAssestsSerializer(serializers.ModelSerializer):
    watchlist_assets=AssetSerializerWithPricing(many=True, read_only=True)
    # latest_asset_pricing=AssetPricingSerializer(many=True, read_only=True,source='watchlist_assets.ticker')
    class Meta:
        model = Watchlist
        fields = ['id','pmp_user','name','created_at','updated_at','watchlist_assets']
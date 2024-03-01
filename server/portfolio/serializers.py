from rest_framework import serializers
from .models import TransactionItem,Portfolio,Watchlist
from assets.serializers import AssetSerializerWithPricingV2,AssetSerializer,AssetSerializerWithPricing
from asset_pricing.serializers import AssetPricingSerializer
from asset_pricing.models import asset_pricing
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
    def to_representation(self, data):
        data = super(PortfolioSerializer, self).to_representation(data)
        data['avgBasis']=data['avg_buy_price']
        data['price']=data['portfolio_asset']['pricing']
        data['marketValue']=data['price']*data['quantity']
        data['costBasis']=data['avgBasis']*data['quantity']
        data['profitLoss']=data['marketValue']-data['costBasis']
        data['percentPL']=data['profitLoss']/data['costBasis']*100
        return data
    


"""
  user= models.ForeignKey(pmp_user, on_delete=models.CASCADE,related_name='portfolio_user_v1')
    portfolio_asset=models.ForeignKey(Asset, on_delete=models.CASCADE,related_name='portfolio_asset_v1',name='portfolio_asset')

    avg_buy_price=models.FloatField(null=True,blank=True)
    avg_sell_price=models.FloatField(null=True,blank=True)
"""
"""
category: "Technology",
      ticker: "AAPL",
      price: 150.5,
      avgBasis: 140.25,
  
      marketValue: 15050.0,
      costBasis: 14025.0,
      profitLoss: 1025.0,
      percentPL: 7.32,
      portfolioPercent: 12.5,
      categoryPercent: 10.2,
"""


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
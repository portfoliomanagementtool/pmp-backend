from rest_framework import serializers
from .models import TransactionItem,Portfolio,Watchlist, PortfolioDailyOverview
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
        data['daypl']=data['portfolio_asset']['daypl']*data['quantity']
        data['daypl_percent']=data['daypl']/data['costBasis']*100
        data.pop('avg_sell_price')
        data.pop('created_at')
        data.pop('updated_at')
        data.pop('user')
        return data
    
class PortfolioDailySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PortfolioDailyOverview
        fields = '__all__'
    def to_representation(self, data):
        data = super(PortfolioDailySerializer, self).to_representation(data)
        response={
            "timestamp":data['timestamp'],
        }
        response['invested_value']={
            "value":data['invested_value'],
            "change":{
                "value":data['change_invested_value'],
                "percentage":data['percent_change_invested_value']
            },
            "type":"green" if data['change_invested_value']>0 else "red"
            }
        response['market_value']={
            "value":data['market_value'],
            "change":{
                "value":data['change_market_value'],
                "percentage":data['percent_change_market_value']
            },
            "type":"green" if data['change_market_value']>0 else "red"
            }
        response['overall_pl']={
            "value":data['overall_pl'],
            "change":{
                "value":data['overall_pl'],
                "percentage":data['overall_pl']/data['invested_value']*100 if data['invested_value']>0 else 0
            },
            "type":"green" if data['overall_pl']>0 else "red"
            }
        response['day_pl']={
            "value":data['change_overall_pl'],
            "change":{
                "value":data['change_overall_pl'],
                "percentage":data['percent_change_overall_pl']
            },
            "type":"green" if data['change_overall_pl']>0 else "red"
            }
        return response
        
        # x={}
        # for i in metrics.keys():
        #     x[i]={
        #         "value":metrics[i],
        #         "change":{
        #             "value":0,
        #             "percentage":0
        #         },
        #         "type":"green"
        #     }
        
        # return data
    # def to_representation(self, data):
    #     data = super(PortfolioSerializer, self).to_representation(data)
    #     data['avgBasis']=data['avg_buy_price']
    #     data['price']=data['portfolio_asset']['pricing']
    #     data['marketValue']=data['price']*data['quantity']
    #     data['costBasis']=data['avgBasis']*data['quantity']
    #     data['profitLoss']=data['marketValue']-data['costBasis']
    #     data['percentPL']=data['profitLoss']/data['costBasis']*100
    #     return data
    

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
class PortfolioDailySerializerForTable(serializers.ModelSerializer):
    
    class Meta:
        model = PortfolioDailyOverview
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
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from .serializers import AssetPricingSerializer,GainLossSerializer
from asset_pricing.models import asset_pricing
from assets.models import Asset
from logging import Logger
from rest_framework import filters
from rest_framework import status,generics
from django.http import JsonResponse

from datetime import timedelta,datetime
from django.db.models import Max, Min
from pmp_auth.decorators import auth_required
import os
import requests
from rest_framework.parsers import FileUploadParser,MultiPartParser
log=Logger("asset_pricing Log")
dummy_data={
  "message": "Top gainers and losers",
  "data": {
    "top_gainers": [
      {
        "ticker": "BTC1",
        "category": "crypto",
        "price": 3502771.7672,
        "day_change_percentage": 10.0,
        "day_change": 350270.0,
        "timestamp": "2023-12-31T00:00:00Z"
      },
      {
        "ticker": "ETH",
        "category": "crypto",
        "price": 189030.1108,
        "day_change_percentage": 1.0,
        "day_change": 1890.0,
        "timestamp": "2023-12-31T00:00:00Z"
      }
    ],
    "top_losers": [
      {
        "ticker": "IBM",
        "category": "stocks",
        "price": 1001,
        "day_change_percentage": -2.7,
        "day_change": -25,
        "timestamp": "2023-12-31T00:00:00Z"
      },
      {
        "ticker": "BTC",
        "category": "crypto",
        "price": 98,
        "day_change_percentage": -2,
        "day_change": -2,
        "timestamp": "2023-12-31T00:00:00Z"
      }
    ]
  }
}
# Create your views here.

# @auth_required
class asset_pricingListCreateView(generics.ListCreateAPIView):
    search_fields = ['market_traded', 'timestamp1']
    filter_backends = (filters.SearchFilter,)
    queryset = asset_pricing.objects.all()
    serializer_class = AssetPricingSerializer
    def get_high_low(self, item,time):
        from datetime import timedelta,datetime
        from django.db.models import Max, Min
        
        
        # Calculate 52-week high and low values for an individual item
        high_low = asset_pricing.objects.filter(
            ticker=item.validated_data["ticker"],
            timestamp1__gte=item.validated_data["timestamp1"]- timedelta(days=time),  # Assuming 'date' is the date field in YourModel
            timestamp1__lte=item.validated_data["timestamp1"]
        ).aggregate(
            high=Max('high'),  # Replace 'high_field_name' with the actual field name for high values
            low=Min('low')     # Replace 'low_field_name' with the actual field name for low values
        )
        return high_low
    
    def perform_create(self, serializer):
        serializer.save()
        hl_52=self.get_high_low(serializer,365)
        hl_month=self.get_high_low(serializer,30)
        hl_overall=self.get_high_low(serializer,20*365)
        day_change=serializer.validated_data["close"]-serializer.validated_data["open"]
        day_change_percentage=day_change/serializer.validated_data["open"]*100
        serializer.save(ft_week_high=hl_52['high'],ft_week_low=hl_52['low'],month_high=hl_month['high'],month_low=hl_month['low'],overall_high=hl_overall['high'],overall_low=hl_overall['low'],day_change=day_change,day_change_percentage=day_change_percentage)
    
    # def list(self,request):
        queryset = self.get_queryset()
    #     start
        
        serializer = AssetPricingSerializer(queryset, many=True)
        return Response(serializer.data)
    def get_queryset(self):
        queryset = super().get_queryset()

        ticket = self.request.query_params.get('ticker', None)
        market_traded = self.request.query_params.get('market_traded', None)
        timestamp1 = self.request.query_params.get('timestamp', None)
        queryset.order_by('-timestamp1')
        if ticket:
            queryset = queryset.filter(ticker=ticket)
        if market_traded:
            queryset = queryset.filter(market_traded=market_traded)
        if timestamp1:
            queryset = queryset.filter(timestamp1=timestamp1)
        



        return queryset

def get_top_gainers_losers(request):   
    try:
        count=request.GET.get('count',5)
        timestamp=request.GET.get('timestamp',datetime.now())
        #top_gainers for last update
        top_gainers = asset_pricing.objects.filter(timestamp1__lte=timestamp).order_by('-timestamp1','-day_change_percentage')[:count]
        top_losers = asset_pricing.objects.filter(timestamp1__lte=timestamp).order_by( '-timestamp1','day_change_percentage')[:count]
        return JsonResponse(status=200,data={"message":"Top gainers and losers","data":{"top_gainers":GainLossSerializer(top_gainers,many=True).data,"top_losers":GainLossSerializer(top_losers,many=True).data}})
    except Exception as e:
        log.error(e)
        return JsonResponse(status=400,data={"message":"Error in getting top gainers"})

def get_dummy_top_gainers_losers(request):
    return JsonResponse(status=200,data=dummy_data)

    
class Latest_Asset_PricingListCreateView(generics.ListCreateAPIView):
    search_fields = ['market_traded', 'timestamp1']
    filter_backends = (filters.SearchFilter,)
    queryset = asset_pricing.objects.all()
    serializer_class = AssetPricingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        ticket = self.request.query_params.get('ticker', None)
        market_traded = self.request.query_params.get('market_traded', None)
        timestamp1 = self.request.query_params.get('timestamp', None)


        if ticket:
            queryset = queryset.filter(ticker=ticket)
        if market_traded:
            queryset = queryset.filter(market_traded=market_traded)
        if timestamp1:
            queryset = queryset.filter(timestamp1=timestamp1)
        # sort queryset by timestamp1 desc
        return queryset.order_by('-timestamp1')


@api_view(['POST'])
@parser_classes([FileUploadParser])
def insert_csv(request):
    f=request.FILES["file"]


    import pandas
    df=pandas.read_csv(f)

    ticker=request.GET.get('ticker')
    df['market_value']=df['close']
    df['timestamp1']=df['timestamp']
    df['currency']="INR"
    df['ticker']=ticker
    # print(df.head(),ticker)
    serializer=AssetPricingSerializer(data=df.to_dict('records'),many=True)
    
    # df['description']=df['name']
    # 
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        for ins in serializer.instance:
            perform_create_1(ins)
            ins.day_change=ins.close-ins.open
            ins.day_change_percentage=ins.day_change/ins.open*100
        
    
    
        
        return Response(status=status.HTTP_200_OK,data={"message":"Excel file received"})
    return Response(status=400,data={"message":"Invalid Excel file"})
required_tickers=["X:BTCUSD",
"X:ETHUSD",
"SPY",
"QQQ",
"VB",
"RWJ",
"EEM",
"EWX",
"EFA",
"VSS",
"GLD",
"XOP",
"XRT",
"XLB",
"XLE",
"XLY",
"XLK",
"XLV",
"XLI",
"XLU",
"XLP",
"XLF",
"XLC"]
def put_daily_pricing_api(request):
    try:
        

        yesterday_date=datetime.now()-timedelta(days=1)
        yesterday_date_str=yesterday_date.strftime("%Y-%m-%d")
        if request.GET and requests.GET.get('date'):
            yesterday_date_str=requests.GET.get('date')
            yesterday_date=datetime.strptime(yesterday_date_str,"%Y-%m-%d")
        api_key=os.environ.get('API_KEY')

        api=f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{yesterday_date_str}?adjusted=true&apiKey={api_key}"
        crypto_api=f"https://api.polygon.io/v2/aggs/grouped/locale/global/market/crypto/{yesterday_date_str}?adjusted=true&apiKey={api_key}"
        response=requests.get(api)
        response_crypto=requests.get(crypto_api)
        data=response.json()
        data_crypto=response_crypto.json()
        if(data['queryCount'] and data['queryCount']>0):
            data=data['results']
            sorted_data=list(filter(lambda x:x['T'] in required_tickers,data))
            today_date=datetime.now()
            for i in sorted_data:
                if(not Asset.objects.filter(ticker=i['T']).exists()):
                    Asset.objects.create(ticker=i['T'],description=i['T'],category="stocks",name=i['T'])
                    
                i['ticker']=i['T']
                i['timestamp1']=today_date
                i['market_value']=i['c']
                i['currency']="USD"
                i['market_traded']="US"
                i['open']=i['o']
                i['high']=i['h']
                i['low']=i['l']
                i['close']=i['c']
                i['volume']=i['v']
                i['day_change']=i['c']-i['o']
                i['day_change_percentage']=i['day_change']/i['o']*100
            
            serializer=AssetPricingSerializer(data=sorted_data,many=True)
            from django.db import transaction
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    for ins in serializer.instance:
                        perform_create_1(ins)
                        ins.day_change=ins.close-ins.open
                        ins.day_change_percentage=ins.day_change/ins.open*100
                    
        
        if(data_crypto['queryCount'] and data_crypto['queryCount']>0):
            data_crypto=list(filter(lambda x:x['T'] in required_tickers,data_crypto['results']))
            
            today_date=datetime.now()
            for i in data_crypto:
                if(not Asset.objects.filter(ticker=i['T']).exists()):
                    Asset.objects.create(ticker=i['T'],description=i['T'],category="crypto",name=i['T'])
                    
                i['ticker']=i['T']
                i['timestamp1']=today_date
                i['market_value']=i['c']
                i['currency']="USD"
                i['market_traded']="US"
                i['open']=i['o']
                i['high']=i['h']
                i['low']=i['l']
                i['close']=i['c']
                i['volume']=i['v']
                i['day_change']=i['c']-i['o']
                i['day_change_percentage']=i['day_change']/i['o']*100
            
            serializer=AssetPricingSerializer(data=data_crypto,many=True)
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    for ins in serializer.instance:
                        perform_create_1(ins)
                        ins.day_change=ins.close-ins.open
                        ins.day_change_percentage=ins.day_change/ins.open*100
                    return JsonResponse({"data":"Success"})
        
        return JsonResponse({"data":"Success"})
    except Exception as e:
        log.error(e)
        return JsonResponse(status=400,data={"message":"Error in getting top gainers"})
    
def perform_create_1(instance):
    hl_52 = get_high_low(instance, 365)
    hl_month = get_high_low(instance, 30)
    hl_overall = get_high_low(instance, 20 * 365)

    
    instance.ft_week_high = hl_52['high']
    instance.ft_week_low = hl_52['low']
    instance.month_high = hl_month['high']
    instance.month_low = hl_month['low']
    instance.overall_high = hl_overall['high']
    instance.overall_low = hl_overall['low']
    instance.save()

def get_high_low(instance, time):
    from datetime import timedelta

    high_low = asset_pricing.objects.filter(
        ticker=instance.ticker,
        timestamp1__gte=instance.timestamp1 - timedelta(days=time),
        timestamp1__lte=instance.timestamp1
    ).aggregate(
        high=Max('high'),
        low=Min('low')
    )
    return high_low


def get_asset_pricings_from_api_last_500_days(request):
    try:
        api_key=os.environ.get('API_KEY')
        ticker=request.GET.get('ticker')
        if ticker==None:
            return JsonResponse(status=400,data={"message":"Ticker not found"})
        #date in this format:2024-03-15
        today_date=datetime.now().date().strftime("%Y-%m-%d")
        asset=Asset.objects.get(ticker=ticker)
        if(asset==None):
            return JsonResponse(status=400,data={"message":"Asset not found"})
        api=None
        if(asset.category=="stocks"):
            api=f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2015-01-15/{today_date}?adjusted=true&sort=desc&limit=100&apiKey={api_key}"
        elif (asset.category=="crypto"):
            api=f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2015-01-15/{today_date}?adjusted=true&sort=desc&limit=100&apiKey={api_key}"
        response=requests.get(api)
        data=response.json()
        print("Received Data")
        if(data['resultsCount'] and data['resultsCount']>0):
            for i in data["results"]:
                i['ticker']=ticker
                i['timestamp1']=datetime.fromtimestamp(i['t']/1000)
                i['market_value']=i['c']
                i['currency']="USD"
                i['market_traded']="US"
                i['open']=i['o']
                i['high']=i['h']
                i['low']=i['l']
                i['close']=i['c']
                i['volume']=i['v']
                i['day_change']=i['c']-i['o']
                i['day_change_percentage']=i['day_change']/i['o']*100
            print("Data Processed")
            serializer=AssetPricingSerializer(data=data['results'],many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                
                return JsonResponse({"data":"Success"})
        return JsonResponse({"data":"False"})

    except Exception as e:
        log.error(e)
        print(e)
        return JsonResponse(status=400,data={"message":"Error in Creating Pricings"})


def recalculate_asset_pricings(request):
    try:
        ticker=request.GET.get('ticker')
        if ticker==None:
            return JsonResponse(status=400,data={"message":"Ticker not found"})
        
        all_asset_pricing=asset_pricing.objects.filter(ticker=ticker).order_by('timestamp1')
        for i in range(1,len(all_asset_pricing)):
            instance=all_asset_pricing[i]
            pre_inst=all_asset_pricing[i-1]
            perform_create_1(instance)
            instance.day_change=pre_inst.close-instance.close
            if pre_inst.close!=0:
                instance.day_change_percentage=instance.day_change/pre_inst.close*100
            else:
                instance.day_change_percentage=100
            
            instance.save()
        return JsonResponse(status=200,data={"message":"Recalculated asset pricing"})

    except Exception as e:
        log.error(e)
        return JsonResponse(status=400,data={"message":"Error in getting top gainers"})


def all_assets_data_to_CSV(request):
    import pandas as pd
    api_key=os.environ.get('API_KEY')
    stock_api=f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-21?adjusted=true&apiKey={api_key}"
    response=requests.get(stock_api)
    stock_data=response.json()
    stock_data=stock_data['results']
    stock_data=pd.DataFrame(stock_data)
    crypto_api=f"https://api.polygon.io/v2/aggs/grouped/locale/global/market/crypto/2023-01-09?adjusted=true&apiKey={api_key}"
    response=requests.get(crypto_api)
    crypto_data=response.json()
    crypto_data=crypto_data['results']
    crypto_data=pd.DataFrame(crypto_data)
    data=pd.concat([stock_data,crypto_data])
    data.to_csv("all_assets_data.csv")
    return JsonResponse({"message":"Data saved to CSV"})
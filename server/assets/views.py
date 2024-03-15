from django.shortcuts import render, redirect
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from .serializers import AssetSerializer,AssetSerializerWithPricing,AssetSerializerWithPricingForTableData
from assets.models import Asset
from logging import Logger
from rest_framework import filters
from rest_framework import status,generics
from rest_framework.parsers import FileUploadParser,MultiPartParser
from pmp_auth.decorators import auth_required
from asset_pricing.models import asset_pricing
log=Logger("Asset Log")
import datetime
# Create your views here.
# @auth_required
class AssetListCreateView(generics.ListCreateAPIView):
    search_fields = ['ticker', 'category', 'name','description']
    filter_backends = (filters.SearchFilter,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializerWithPricingForTableData

    def get(self, request):
        print("custom list")
        
        if ticker:
            queryset = self.get_queryset()
            response = super().list(request)
            serializer = self.get_serializer(queryset, many=True)
            # ticker=request.query_params.get('ticker',None)
            # start=request.query_params.get('start',None)
            # end=request.query_params.get('end',None)
            ticker=request.query_params.get('ticker',None)
            end=datetime.datetime.now()
            month_ago=end-datetime.timedelta(days=30)
            year_ago=end-datetime.timedelta(days=365)
            six_month_ago=end-datetime.timedelta(days=180)
        
            try:
                for asset_data in serializer.data:
                    ticker = asset_data.get('ticker')
                    if ticker:
                        # Fetch pricing data based on ticker
                        before_start = asset_pricing.objects.filter(ticker=ticker).earliest('timestamp1')
                        before_end = asset_pricing.objects.filter(ticker=ticker).latest('timestamp1')
                        before_month=asset_pricing.objects.filter(ticker=ticker,timestamp1__lte=month_ago).latest('timestamp1')
                        before_year=asset_pricing.objects.filter(ticker=ticker,timestamp1__lte=year_ago).latest('timestamp1')
                        before_six_month=asset_pricing.objects.filter(ticker=ticker,timestamp1__lte=six_month_ago).latest('timestamp1')
                        before_first_date_of_this_year=asset_pricing.objects.filter(ticker=ticker,timestamp1__lte=datetime.datetime(end.year,1,1)).latest('timestamp1')

                        total_change=before_end.market_value-before_start.market_value
                        total_change_percentage=(total_change/before_start.market_value)*100

                        
                        changes={
                            "default":{
                                "change":asset_data['day_change'],
                                "change_percentage":asset_data['day_change_percentage']
                            },
                            "one_month":{
                                "change":total_change,
                                "change_percentage":total_change_percentage
                            },
                            "six_month":{
                                "change":total_change,
                                "change_percentage":total_change_percentage
                            },
                            "ytd":{
                                "change":total_change,
                                "change_percentage":total_change_percentage
                            },
                            "six_month":{
                                "change":total_change,
                                "change_percentage":total_change_percentage
                            },
                            "all":{
                                "change":total_change,
                                "change_percentage":total_change_percentage
                            }
                        }

                        if before_month and before_month.market_value>0:
                            month_change=before_end.market_value-before_month.market_value
                            month_change_percentage=(month_change/before_month.market_value)*100
                            changes["one_month"]={
                                "change":month_change,
                                "change_percentage":month_change_percentage
                            }
                        if before_year and before_year.market_value>0:
                            year_change=before_end.market_value-before_year.market_value
                            year_change_percentage=(year_change/before_year.market_value)*100
                            changes["one_year"]={
                                "change":year_change,
                                "change_percentage":year_change_percentage
                            }
                        if before_six_month and before_six_month.market_value>0:
                            six_month_change=before_end.market_value-before_six_month.market_value
                            six_month_change_percentage=(six_month_change/before_six_month.market_value)*100
                            changes["six_month"]={
                                "change":six_month_change,
                                "change_percentage":six_month_change_percentage
                            }
                        if before_first_date_of_this_year and before_first_date_of_this_year.market_value>0:
                            ytd_change=before_end.market_value-before_first_date_of_this_year.market_value
                            ytd_change_percentage=(ytd_change/before_first_date_of_this_year.market_value)*100
                            changes["ytd"]={
                                "change":ytd_change,
                                "change_percentage":ytd_change_percentage
                            }
                        

                        
                        
                        
                        # Add day_change and day_change_percentage to asset_data
                        modified_asset_data = asset_data.copy()
            
                        # Add change and change_percentage to modified_asset_data
                        modified_asset_data['changes'] = changes
                        return Response([modified_asset_data])
            except Exception as e:
                print(e)
            # return Response([serializer.data])
        return response


    def get_queryset(self):
        queryset = super().get_queryset()

        ticker = self.request.query_params.get('ticker', None)
        category = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)

        if ticker:
            queryset = queryset.filter(ticker=ticker)
        if category:
            queryset = queryset.filter(category=category)
        if name:
            queryset = queryset.filter(name=name)
        if description:
            queryset = queryset.filter(description=description)

        return queryset

class AssetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializerWithPricing
    def get_queryset(self):
        queryset = super().get_queryset()

        ticker = self.request.query_params.get('ticker', None)
        category = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)

        if ticker:
            queryset = queryset.filter(ticker=ticker)
        if category:
            queryset = queryset.filter(category=category)
        if name:
            queryset = queryset.filter(name=name)
        if description:
            queryset = queryset.filter(description=description)

        return queryset


@api_view(['POST'])
@parser_classes([FileUploadParser])
def insert_csv(request):
    f=request.FILES["file"]


    import pandas
    df=pandas.read_excel(f,sheet_name='Assets')
    # print(df.head()['Ticker','Category','Name'])
    df.rename(columns={'Ticker':'ticker','Category':'category','Name':'name'},inplace=True)
    print(df.head())
    df['description']=df['name']
    serializer=AssetSerializer(data=df.to_dict('records'),many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK,data={"message":"Excel file received"})
    return Response(status=400,data={"message":"Invalid Excel file"})
@api_view(['POST'])
@parser_classes([FileUploadParser])
def insert_csv_alphavantage(request):
    f=request.FILES["file"]


    import pandas
    df=pandas.read_excel(f,sheet_name='Assets')
    # print(df.head()['Ticker','Category','Name'])
    df.rename(columns={'Ticker':'ticker','Category':'category','Name':'name'},inplace=True)
    print(df.head())
    df['description']=df['name']
    serializer=AssetSerializer(data=df.to_dict('records'),many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK,data={"message":"Excel file received"})
    return Response(status=400,data={"message":"Invalid Excel file"})


# @api_view(['GET'])
# def get_asset(request):
#     assets=Asset.objects.all()
#     serializer=AssetSerializer(assets,many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def insert_asset(request):
#         serializer=AssetSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#              serializer.save()
#         return Response(serializer.data)

# @api_view(['POST'])
# def edit_asset(request,pk):
#     if request.data==None:
#          return Response(status=status.HTTP_400_BAD_REQUEST)
#     # (request)
#     asset=Asset.objects.get(ticker=pk)
    
#     serializer=AssetSerializer(data=asset)
#     print(serializer)
#     # return Response()
#     if serializer.is_valid():
#             serializer.update(request.data)
#             serializer.save()
#     return Response(serializer.data)

# def remove_asset(request, pk):
#     assets = Asset.objects.get(id=pk)

#     if request.method == 'POST':
#         assets.delete()
#         return redirect('/show')

#     context = {
#         'assets': assets,
#     }

#     return render(request, 'delete.html', context)
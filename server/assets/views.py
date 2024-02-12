from django.shortcuts import render, redirect
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from .serializers import AssetSerializer,AssetSerializerWithPricing
from assets.models import Asset
from logging import Logger
from rest_framework import filters
from rest_framework import status,generics
from rest_framework.parsers import FileUploadParser,MultiPartParser
from pmp_auth.decorators import auth_required
log=Logger("Asset Log")
# Create your views here.
# @auth_required
class AssetListCreateView(generics.ListCreateAPIView):
    search_fields = ['ticker', 'category', 'name','description']
    filter_backends = (filters.SearchFilter,)
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
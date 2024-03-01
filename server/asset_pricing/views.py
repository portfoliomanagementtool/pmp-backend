from django.shortcuts import render, redirect
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from .serializers import AssetPricingSerializer
from asset_pricing.models import asset_pricing
from logging import Logger
from rest_framework import filters
from rest_framework import status,generics
from pmp_auth.decorators import auth_required
log=Logger("asset_pricing Log")
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
        serializer.save(ft_week_high=hl_52['high'],ft_week_low=hl_52['low'],month_high=hl_month['high'],month_low=hl_month['low'],overall_high=hl_overall['high'],overall_low=hl_overall['low'])
        
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

        return queryset


    
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

        return queryset


    
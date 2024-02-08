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


    
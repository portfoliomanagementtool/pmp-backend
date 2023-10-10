from django.shortcuts import render, redirect
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from .serializers import asset_pricingSerializer
from asset_pricing.models import asset_pricing
from logging import Logger
from rest_framework import status,generics
from pmp_auth.decorators import auth_required
log=Logger("asset_pricing Log")
# Create your views here.
# @auth_required
class asset_pricingListCreateView(generics.ListCreateAPIView):
    queryset = asset_pricing.objects.all()
    serializer_class = asset_pricingSerializer

class asset_pricingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = asset_pricing.objects.all()
    serializer_class = asset_pricingSerializer



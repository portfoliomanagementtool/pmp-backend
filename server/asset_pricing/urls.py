from django.urls import path
from . import views

urlpatterns = [
    path('asset_pricing/', views.asset_pricingListCreateView.as_view(), name='asset-pricing-list-create'),
    
]


from django.urls import path
from . import views

urlpatterns = [
    path('asset_pricing/create', views.asset_pricingListCreateView.as_view(), name='asset-pricing-list-create'),
    path('asset_pricing', views.asset_pricingListCreateView.as_view(), name='asset-pricing-list'),
    path('asset_pricing/latest', views.Latest_Asset_PricingListCreateView.as_view(), name='asset-pricing-list'),
    path('asset_pricing/bulk_upload', views.insert_csv, name='bulk_upload'),
    path('asset_pricing/top_gainers_losers', views.get_dummy_top_gainers_losers, name='top_gainers_losers'),
    path('asset_pricing/recalculate_asset_pricings', views.recalculate_asset_pricings, name='top_gainers_losers'),
    
]


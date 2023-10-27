from django.urls import path
from . import views

urlpatterns = [
    path('asset_pricing/', views.AssetListCreateView.as_view(), name='asset-pricing-list-create'),
    path('asset_pricing/<str:pk>/',views. AssetRetrieveUpdateDestroyView.as_view(), name='asset-pricing-detail'),
    
]


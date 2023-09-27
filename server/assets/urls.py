from django.urls import path
from . import views

urlpatterns = [
    path('assets/', views.AssetListCreateView.as_view(), name='asset-list-create'),
    path('assets/<str:pk>/',views. AssetRetrieveUpdateDestroyView.as_view(), name='asset-detail'),

    # path('add',views.insert_asset),
    # path('edit/<str:pk>', views.edit_asset, name='edit-asset'),
    # path('remove/<str:pk>', views.remove_asset, name='remove-asset'),
]

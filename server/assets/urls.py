from django.urls import path
from . import views

urlpatterns = [
    path('', views.insert_asset, name='insert-asset'),
    path('show/', views.show_asset, name='show-asset'),
    path('edit/<int:pk>', views.edit_asset, name='edit-asset'),
    path('remove/<int:pk>', views.remove_asset, name='remove-asset'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('users/test', views.list_users),
    
]


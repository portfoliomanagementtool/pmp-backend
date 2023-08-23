from django.urls import path

from . import views

urlpatterns = [
    path("verify_token", views.verify_token), #This is a verify path. This was made during creation of code. to be used as middleware than a API
]
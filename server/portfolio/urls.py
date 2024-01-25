from django.urls import path
from . import views


urlpatterns = [
    path('users/list', views.list_users),
    path('users/create', views.UserListCreateView.as_view(), name='pmp-create-users'),
    path('users/<str:pk>/delete/', views.UserRetrieveUpdateDestroyView.as_view(), name='pmp-delete-user'),

]


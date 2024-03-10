from django.urls import path
from . import views

urlpatterns = [
    path('get_notifications', views.get_notifications, name='get_notifications'),
    path('mark_as_read',views.mark_as_read, name='mark_read'),
    path('mark_as_read_all',views.mark_as_read_all, name='mark_read_all'),

    # path('add',views.insert_asset),
    # path('edit/<str:pk>', views.edit_asset, name='edit-asset'),
    # path('remove/<str:pk>', views.remove_asset, name='remove-asset'),
]


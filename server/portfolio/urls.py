from django.urls import path
from . import views


urlpatterns = [
    path('buy', views.buy_asset),
    path('sell', views.sell_asset),
    path('transactions', views.list_transactions),
    path('portfolios', views.list_portfolio),
    path('watchlist', views.list_watchlists),
    path('watchlist/add', views.add_watchlist),
    path('watchlist/delete', views.delete_watchlist),
    path('watchlist/<int:watchlist_id>', views.list_assets_in_watchlist),
    path('watchlist/<int:watchlist_id>/add', views.add_asset_to_watchlist),
    path('watchlist/<int:watchlist_id>/delete', views.delete_asset_from_watchlist),
    path('getmetrics', views.get_user_metrics),
    
    path('create_daily_portfolio', views.create_portfolio_api),
    path('get_daily_portfolio', views.get_portfolio_api),
    
]


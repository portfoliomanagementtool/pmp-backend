from django.shortcuts import render
from django.http import JsonResponse
from pmp_auth.decorators import auth_required
from .models import TransactionItem,Watchlist,Portfolio
import json
from assets.models import Asset
from .serializers import TransactionItemSerializer,PortfolioSerializer
from django.db import transaction
# Create your views here.
@auth_required
def buy_asset(request):
    try:
        with transaction.atomic():

            user=request.pmp_user
            data=json.loads(request.body.decode("utf-8"))
            asset=Asset.objects.get(ticker=data["ticker"])
            TransactionItem.objects.create(user=user,transaction_asset=asset,quantity=data["quantity"],buy_price=data["price"])
            exitst=Portfolio.objects.filter(user=user,portfolio_asset=asset)
            if exitst.count()==0:
                Portfolio.objects.create(user=user,portfolio_asset=asset,quantity=data["quantity"],avg_buy_price=data["price"])
            else:
                portfolio=exitst.first()
                total_quantity=portfolio.quantity+data["quantity"]
                avg_buy_price=(portfolio.quantity*portfolio.avg_buy_price+data["quantity"]*data["price"])/total_quantity
                portfolio.quantity=total_quantity
                portfolio.avg_buy_price=avg_buy_price
                portfolio.save()
            return JsonResponse(status=200,data={"message":"Asset bought successfully"})
        
        return JsonResponse(status=400,data={"message":"Error while buying the Asset"})

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while buying the Asset"})
@auth_required
def sell_asset(request):
    try:
        with transaction.atomic():

            user=request.pmp_user
            data=json.loads(request.body.decode("utf-8"))
            asset=Asset.objects.get(ticker=data["ticker"])
            TransactionItem.objects.create(user=user,transaction_asset=asset,quantity=data["quantity"],sell_price=data["price"])
            exitst=Portfolio.objects.filter(user=user,portfolio_asset=asset)
            if exitst.count()==0:
                raise Exception("Asset not present in portfolio")
            else:
                portfolio=exitst.first()
                total_quantity=portfolio.quantity-data["quantity"]
                if(total_quantity<0):
                    raise Exception("Not enough quantity to sell")
                portfolio.quantity=total_quantity
                portfolio.save()
            return JsonResponse(status=200,data={"message":"Asset bought successfully"})
        
        return JsonResponse(status=400,data={"message":"Error while buying the Asset"})

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":e.message if hasattr(e,"message") else "Error while buying the Asset"})

@auth_required
def list_transactions(request):
    try:
        user=request.pmp_user
        transactions=TransactionItem.objects.filter(user=user)

        return JsonResponse(status=200,data={"message":"Portfolio items fetched successfully","data":TransactionItemSerializer(transactions,many=True).data})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching portfolio items"})
    

@auth_required
def list_portfolio(request):
    try:
        user=request.pmp_user
        portfolio=Portfolio.objects.filter(user=user).filter(quantity__gt=0)
        categories={}
        total_investment=0
        for item in portfolio:
            if item.portfolio_asset.category not in categories:
                categories[item.portfolio_asset.category]={"value":0}
            categories[item.portfolio_asset.category]["value"]+=item.quantity*item.avg_buy_price
            total_investment+=item.quantity*item.avg_buy_price
        for category in categories:
            categories[category]["value"]=round(categories[category]["value"],2)
            categories[category]["percentage"]=round(categories[category]["value"]/total_investment*100,2)
        return JsonResponse(status=200,data={"message":"Portfolio items fetched successfully","assets":PortfolioSerializer(portfolio,many=True).data,"categories":categories})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching portfolio items"})
def list_watchlists(request):
    pass

def add_watchlist(request):
    pass

def delete_watchlist(request):
    pass

def list_assets_in_watchlist(request):
    pass

def add_asset_to_watchlist(request):
    pass

def delete_asset_from_watchlist(request):
    pass


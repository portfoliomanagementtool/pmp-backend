from django.shortcuts import render
from django.http import JsonResponse
from pmp_auth.decorators import auth_required
from .models import TransactionItem,Watchlist,Portfolio, PortfolioDailyOverview
import json
from assets.models import Asset
from asset_pricing.models import asset_pricing
from .serializers import TransactionItemSerializer,PortfolioSerializer,WatchlistSerializer,WatchlistWithAssestsSerializer ,PortfolioDailySerializer
from django.db import transaction
from notifications.views import create_notification
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
            _create_daily_portfolio(user,datetime.datetime.now(),False)
            create_notification(user,"BUY","You have bought "+str(data["quantity"])+" of "+asset.ticker+" at "+str(data["price"])+" per unit")
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
            
            _create_daily_portfolio(user,datetime.datetime.now(),False)
            create_notification(user,"SELL","You have sold "+str(data["quantity"])+" of "+asset.ticker+" at "+str(data["price"])+" per unit")
            return JsonResponse(status=200,data={"message":"Asset sold successfully"})
        
        return JsonResponse(status=400,data={"message":"Error while buying the Asset"})

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":e.message if hasattr(e,"message") else "Error while buying the Asset"})

@auth_required
def list_transactions(request):
    try:
        user=request.pmp_user
        transactions=TransactionItem.objects.filter(user=user).order_by('-created_at')

        return JsonResponse(status=200,data={"message":"Transactions fetched successfully","data":TransactionItemSerializer(transactions,many=True).data})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching portfolio items"})
    

@auth_required
def list_portfolio(request):
    try:
        user=request.pmp_user
        portfolio=Portfolio.objects.filter(user=user).filter(quantity__gt=0)
        if(request.GET.get('category')!=None):
            portfolio=portfolio.filter(portfolio_asset__category=request.GET.get('category'))
        if(request.GET.get('ticker')!=None):
            portfolio=portfolio.filter(portfolio_asset__ticker=request.GET.get('ticker'))
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
@auth_required
def list_watchlists(request):
    try:
        user=request.pmp_user
        watchlists=Watchlist.objects.filter(pmp_user=user)
        if watchlists is None:
            Watchlist.objects.create(pmp_user=user,name="Default")
        watchlists=Watchlist.objects.filter(pmp_user=user)
        return JsonResponse(status=200,data={"message":"Fetched a Watchlist Successfully","data":WatchlistSerializer(watchlists,many=True).data})
    
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching the Watchlist"})

@auth_required
def add_watchlist(request):
    try:
        user=request.pmp_user
        data=json.loads(request.body.decode("utf-8"))
        Watchlist.objects.create(pmp_user=user,name=data["name"])
        return JsonResponse(status=200,data={"message":"Added a Watchlist Successfully"})
    
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching the Watchlist"})


    pass

def delete_watchlist(request):
    pass
@auth_required
def list_assets_in_watchlist(request,watchlist_id):
    try:
        user=request.pmp_user
        watchlists=Watchlist.objects.get(id=watchlist_id)
        if watchlists is None:
            return JsonResponse(status=400,data={"message":"Watchlist not found"})
        if watchlists.pmp_user!=user:
            return JsonResponse(status=400,data={"message":"User does not have access to this watchlist"})
        
        return JsonResponse(status=200,data={"message":"Fetched a Watchlist Successfully","data":WatchlistWithAssestsSerializer(watchlists).data})
    
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching the Watchlist"})

@auth_required
def add_asset_to_watchlist(request,watchlist_id):
    try:
        user=request.pmp_user
        data=json.loads(request.body.decode("utf-8"))
        watchlist=Watchlist.objects.get(id=watchlist_id)
        if watchlist is None:
            return JsonResponse(status=400,data={"message":"Watchlist not found"})
        if watchlist.pmp_user!=user:
            return JsonResponse(status=400,data={"message":"User does not have access to this watchlist"})
        
        asset=Asset.objects.get(ticker=data["ticker"])
        if asset is None:
            return JsonResponse(status=400,data={"message":"Asset not found"})
        
        watchlist.watchlist_assets.add(asset)
        watchlist.save()

        return JsonResponse(status=200,data={"message":"Added asset to Watchlist Successfully"})
    
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Watchlist or Asset Not Found"})

@auth_required
def delete_asset_from_watchlist(request,watchlist_id):
    try:
        user=request.pmp_user
        data=json.loads(request.body.decode("utf-8"))
        watchlist=Watchlist.objects.get(id=watchlist_id)
        if watchlist is None:
            return JsonResponse(status=400,data={"message":"Watchlist not found"})
        if watchlist.pmp_user!=user:
            return JsonResponse(status=400,data={"message":"User does not have access to this watchlist"})
        
        asset=Asset.objects.get(ticker=data["ticker"])
        if asset is None:
            return JsonResponse(status=400,data={"message":"Asset not found"})
        watchlist.watchlist_assets.remove(asset)
        watchlist.save()

        return JsonResponse(status=200,data={"message":"Removed asset to Watchlist Successfully"})
    
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Watchlist or Asset Not Found"})


@auth_required
def get_user_metrics(request):
    try:
        user=request.pmp_user
        portfolio=Portfolio.objects.filter(user=user).filter(quantity__gt=0)
        total_investment=0
        latest_portfolio=PortfolioDailyOverview.objects.filter(user=user).order_by('-timestamp').first()
        if(latest_portfolio==None): 
            tm=datetime.datetime.now()-datetime.timedelta(days=1)
            _create_daily_portfolio(user,tm,False)
            latest_portfolio=PortfolioDailyOverview.objects.filter(user=user).order_by('-timestamp').first()
        

        categories={

        }
        for item in portfolio:
            if item.portfolio_asset.category not in categories:
                categories[item.portfolio_asset.category]={"value":0}
            categories[item.portfolio_asset.category]["value"]+=item.quantity*item.avg_buy_price
            total_investment+=item.quantity*item.avg_buy_price

        response_met=[]
        for category in categories:
            
            categories[category]["value"]=round(categories[category]["value"],2)
            categories[category]["percentage"]=round(categories[category]["value"]/total_investment*100,2)
        
        
        
        return JsonResponse(status=200,data={"message":"Portfolio items fetched successfully","categories":categories,'metrics':PortfolioDailySerializer(latest_portfolio).data})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while fetching portfolio items"})
    
import datetime
#This is used to create portfolio daily  and can be used with cron or similar schedulers
def _create_daily_portfolio(user_id,timestamp=datetime.datetime.now(),res=True):
    try:
        # create_notification(user_id,"UPDATE","Latest daily portfolio created")        
        portfolio=Portfolio.objects.filter(user=user_id).filter(quantity__gt=0)
        total_investment=0
        metrics={
            "market_value":0,
            "invested_value":0,
            "overall_pl":0
        }
        
        for item in portfolio:
            current_asset_pricing=asset_pricing.objects.filter(ticker=item.portfolio_asset.ticker)
            if(current_asset_pricing.first()!=None):
                metrics['market_value']+=current_asset_pricing.first().market_value*item.quantity
            total_investment+=item.quantity*item.avg_buy_price

        response_met=[]
        metrics['invested_value']=total_investment
        metrics['overall_pl']=metrics["market_value"]-metrics["invested_value"]


        with transaction.atomic():
            last_portfolio=PortfolioDailyOverview.objects.filter(user=user_id).filter(timestamp__lt=timestamp.date()).order_by('-timestamp').first()
            if last_portfolio!=None:
                metrics['change_invested_value']=metrics['invested_value']-last_portfolio.invested_value
                metrics['change_market_value']=metrics['market_value']-last_portfolio.market_value
                metrics['change_overall_pl']=metrics['overall_pl']-last_portfolio.overall_pl
                if last_portfolio.invested_value==0:
                    metrics['percent_change_invested_value']=100 if metrics['invested_value']>0 else 0
                else:
                    metrics['percent_change_invested_value']=round(metrics['change_invested_value']/last_portfolio.invested_value*100,2)
                if last_portfolio.market_value==0:
                    metrics['percent_change_market_value']=100 if metrics['market_value']>0 else 0
                else:
                    metrics['percent_change_market_value']=round(metrics['change_market_value']/last_portfolio.market_value*100,2)
                if last_portfolio.overall_pl==0:
                    metrics['percent_change_overall_pl']=100 if metrics['overall_pl']>0 else 0
                else:
                    metrics['percent_change_overall_pl']=round(metrics['change_overall_pl']/last_portfolio.overall_pl*100,2)
            
            portf=PortfolioDailyOverview.objects.create(user=user_id,timestamp=timestamp,**metrics)
            if res:
                return portf

            return JsonResponse(status=200,data={"message":"Daily Portfolio created successfully"})
        return JsonResponse(status=400,data={"message":"Error while creating daily portfolio"})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while creating daily portfolio"})
    
    
@auth_required
def create_portfolio_api(req):
    try:
        data={}
        if(req.body!=b''):
            data=json.loads(req.body.decode("utf-8"))
        user_id=req.pmp_user
        timestamp=datetime.datetime.now()
        if data.get("timestamp")!=None:
            timestamp=data["timestamp"]
        return _create_daily_portfolio(user_id,timestamp)
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while creating daily portfolio1"})
    

@auth_required
def get_portfolio_api(req):
    try:
        latest_portfolio=PortfolioDailyOverview.objects.filter(user=req.pmp_user).order_by('-timestamp').first()
        if latest_portfolio==None:
            return JsonResponse(status=400,data={"message":"No portfolio found"})
        return JsonResponse(status=200,data={"message":"Fetched portfolio successfully","data":PortfolioDailySerializer(latest_portfolio).data})
    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while creating daily portfolio1"})
    


@auth_required
def get_monthly_investments(req):
    try:
        invested_value={}
        transactions=TransactionItem.objects.filter(user=req.pmp_user)
        for transaction in transactions:
            key=transaction.created_at.strftime("%B-%Y")
            if key not in invested_value:
                invested_value[key]=0
            if transaction.buy_price!=None:
                invested_value[key]+=transaction.buy_price*transaction.quantity
            if transaction.sell_price!=None:
                invested_value[key]-=transaction.sell_price*transaction.quantity
        return JsonResponse(status=200,data={"message":"Fetched monthly investments successfully","data":invested_value})

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while creating daily portfolio1"})
    

@auth_required
def get_daily_investments(req):
    try:
        invested_value={}
        transactions=TransactionItem.objects.filter(user=req.pmp_user)
        for transaction in transactions:
            key=transaction.created_at.strftime("%d-%m-%Y")
            if key not in invested_value:
                invested_value[key]=0
            if transaction.buy_price!=None:
                invested_value[key]+=transaction.buy_price*transaction.quantity
            if transaction.sell_price!=None:
                invested_value[key]-=transaction.sell_price*transaction.quantity
        return JsonResponse(status=200,data={"message":"Fetched monthly investments successfully","data":invested_value})

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={"message":"Error while getting daily investments"})
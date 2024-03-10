from django.http import HttpResponse
from django.http.response import JsonResponse
from utils.auth import verify_token as jwt_verify
from django.views.decorators.csrf import csrf_exempt
from pmp_user.models import pmp_user as PMPUser

# from portfolio.views import _create_daily_portfolio
@csrf_exempt
def auth_required(function):
    @csrf_exempt
    def wrapper(request,*args,**kwargs):
        token=None
        user=None
        try:
                token=request.headers["UserId"]
            
        except KeyError:
            return JsonResponse(status=403,data={"message":"Token missing. Please add Token to header as Authorization : Bearer ..."})
        try:
            ## this is temporary solution as the frontend is not sending the user token 
            user=PMPUser.objects.get(email=request.headers["UserId"])
        except KeyError:
            return JsonResponse(status=400,data={"message":"User missing. Please add a header as UserId"})
        except Exception as e:
            
            try:
                user=PMPUser.objects.create(email=request.headers["UserId"])
            except Exception as e:
                print(e)
                return JsonResponse(status=400,data={"message":"Error in adding User"})
            # print(e)
            # return JsonResponse(status=400,data={"message":"User missing. Please add a header as UserId"})
        # token=request.headers["Authorization"]
        # user=request.GET["user"]
        request.pmp_user=user
        request.is_admin=False
        # authorised=jwt_verify(token,user)
        if(request.pmp_user):
            return function(request,*args,**kwargs)
        return JsonResponse({"status_code": 403,"status_msg":"Invalid Token"},status=403, safe=False)
    return wrapper
#TODO: Add admin_required decorator

def admin_required(function):
    def wrapper(request,*args,**kwargs):
        token=None
        user=None
        try:
            token=request.headers["Authorization"]
        except KeyError:
            return JsonResponse(status=403,data={"message":"Token missing. Please add Token to header as Authorization : Bearer ..."})
        try:
            user=request.GET["user"]
        except KeyError:
            return JsonResponse(status=400,data={"message":"User missing. Please add a parameter as user=user_id"})
        except Exception as e:
            print(e)
            return JsonResponse(status=400,data={"message":"User missing. Please add a parameter as user=user_id"})
        token=request.headers["Authorization"]
        user=request.GET["user"]

        if(token==None):
            return JsonResponse(status=403,data={"message":"Token missing. Please add Token to header as Authorization : Bearer ..."})
        if(user==None):
            return JsonResponse(status=400,data={"message":"User missing. Please add a parameter as user=user_id"})
        request.user=user
        request.is_admin=False
        authorised=jwt_verify(token,user)
        if(authorised):
            return function(request,*args,**kwargs)
        return JsonResponse({"status_code": 403,"status_msg":"Invalid Token"},status=403, safe=False)
    return wrapper






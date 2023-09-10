from django.http import HttpResponse
from django.http.response import JsonResponse
from utils.auth import verify_token as jwt_verify

def verify_token(request):

    if request.method=='GET':
        token=request.headers["Authorization"] #Takes the Access Token
        user=request.GET["user"] #Takes the "user" param from url 
        if(token==None):
            return JsonResponse(status=403,data={"message":"Token missing. Please add Token to header as Authorization : Bearer ..."})
        if(user==None):
            return JsonResponse(status=400,data={"message":"User missing. Please add a parameter as user=user_id"})
            
        authorised=jwt_verify(token,user)
        if(authorised):
            return JsonResponse({"status":200,"message":"User Successfully Logged In"},safe=False)
        return JsonResponse({"status_code": 403,"status_msg":"Invalid Token"},status=403, safe=False)
    else:
        return JsonResponse(status=400,data={"message":"Invalid request. This path is valid for GET request only"})


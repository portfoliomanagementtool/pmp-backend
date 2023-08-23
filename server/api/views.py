from django.http import HttpResponse
from django.http.response import JsonResponse
from utils.auth import verify_token as jwt_verify

def verify_token(request):
    token=request.headers["Authorization"] #Takes the Access Token
    user=request.GET["user"] #Takes the "user" param from url 
    authorised=jwt_verify(token,user)
    if(authorised):
        return JsonResponse({"status":200,"message":"User Successfully Logged In"},safe=False)
    return JsonResponse({"status_code": 403,"status_msg":"Invalid Token"},status=403, safe=False)
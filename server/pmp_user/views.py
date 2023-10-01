from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from pmp_auth.decorators import auth_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@auth_required
@csrf_exempt
@api_view(['GET'])
def list_users(request):
    return Response({"message":"List of users"},status=200)

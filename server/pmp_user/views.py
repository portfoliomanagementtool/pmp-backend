from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from pmp_auth.decorators import auth_required
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from pmp_user.models import pmp_user
from logging import Logger
from rest_framework import filters, status, generics
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
@auth_required
@csrf_exempt
@api_view(['GET'])
def list_users(request):
    return Response({"message":"List of users"},status=200)


# @auth_required
class UserListCreateView(generics.ListCreateAPIView):
    search_fields = ['uuid', 'name', 'email','phone']
    filter_backends = (filters.SearchFilter,)
    queryset = pmp_user.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = super().get_queryset()

        uuid = self.request.query_params.get('uuid', None)
        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)
        phone = self.request.query_params.get('phone', None)

        if uuid:
            queryset = queryset.filter(uuid=uuid)
        if name:
            queryset = queryset.filter(name=name)
        if email:
            queryset = queryset.filter(email=email)
        if phone:
            queryset = queryset.filter(phone=phone)

        return queryset

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = pmp_user.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = super().get_queryset()

        uuid = self.request.query_params.get('uuid', None)
        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)
        phone = self.request.query_params.get('phone', None)

        if uuid:
            queryset = queryset.filter(uuid=uuid)
        if name:
            queryset = queryset.filter(name=name)
        if email:
            queryset = queryset.filter(email=email)
        if phone:
            queryset = queryset.filter(phone=phone)

        return queryset
from rest_framework.serializers import ModelSerializer
from .models import pmp_user

class UserSerializer(ModelSerializer):
    class Meta:
        model=pmp_user
        fields='__all__'
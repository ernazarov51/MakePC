from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User
from apps.serializers import RegisterModelSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Create your views here.
class RegisterCreateAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer
    queryset = User.objects.all()


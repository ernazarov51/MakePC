from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User
from apps.serializers import RegisterModelSerializer, CustomTokenObtainPairSerializer, ProfileModelSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Create your views here.
class RegisterCreateAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer
    queryset = User.objects.all()

@extend_schema(tags=['Customer'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api_view(request):
    user=request.user
    serializer=ProfileModelSerializer(request.user)
    if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



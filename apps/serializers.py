from django.contrib.auth.hashers import make_password
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import User
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['role'] = self.user.role

        return data
class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','role','email','password']

    def validate(self, attrs):
        attrs['username']=attrs['email']
        attrs['password']=make_password(attrs['password'])
        return attrs


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','email','role']

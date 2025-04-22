from django.contrib.auth.hashers import make_password
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import User, Post, Comment


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['role'] = self.user.role

        return data


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        attrs['username'] = attrs['email']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role']


class AllPostForUserModelSerializer(ModelSerializer):
    text = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text']

    def get_text(self, obj):
        return obj.text[:100] if len(obj.text) >= 100 else obj.text


class SellerCommentSerializer(ModelSerializer):
    fullname = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']

    def get_fullname(self, obj):
        return obj.first_name + ' ' + obj.last_name if obj.first_name + ' ' + obj.last_name != ' ' else None


class CommentModelSerializer(ModelSerializer):
    seller = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'seller']

    def get_seller(self, obj):
        return SellerCommentSerializer(obj.seller).data


class PostDetailModelSerializer(ModelSerializer):
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'customer', 'phone_number', 'price', 'comments']

    def get_comments(self, obj):
        return CommentModelSerializer(obj.comments, many=True).data


class SellerCommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post']
        depth = 1


class PostCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'price', 'phone_number']

    def validate(self, attrs):
        attrs['customer'] = self.context['request'].user
        return attrs


class CommentCreateModelSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields=['text']

    def validate(self, attrs):
        attrs['seller']=self.context['request'].user
        attrs['post']=self.context['post']
        return attrs
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User, Post, Comment
from apps.serializers import RegisterModelSerializer, CustomTokenObtainPairSerializer, ProfileModelSerializer, \
    AllPostForUserModelSerializer, PostDetailModelSerializer, SellerCommentModelSerializer, PostCreateModelSerializer, \
    CommentCreateModelSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Create your views here.
class RegisterCreateAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegisterModelSerializer
    queryset = User.objects.all()


@extend_schema(tags=['Customer'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api_view(request):
    user = request.user
    serializer = ProfileModelSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Customer'])
class PostsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = AllPostForUserModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(customer=self.request.user)
        return queryset


@extend_schema(tags=['Customer'])
class PostDetailRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = PostDetailModelSerializer


@extend_schema(tags=['Seller'])
class SellerCommentAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = SellerCommentModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(seller=self.request.user)
        return queryset


@extend_schema(tags=['Customer'], request=PostCreateModelSerializer)
class PostCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateModelSerializer
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@extend_schema(tags=['Seller'])
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateModelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['request']=self.request
        post_id=self.kwargs['post_id']
        print(post_id)
        post=Post.objects.filter(id=post_id)
        context['post_id']=post.id
        return context


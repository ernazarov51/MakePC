from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User, Post, Comment, Category, Product
from apps.permissions import IsSellerPermission, IsCustomerPermission, IsAdminPermission
from apps.serializers import RegisterModelSerializer, CustomTokenObtainPairSerializer, ProfileModelSerializer, \
    AllPostForUserModelSerializer, PostDetailModelSerializer, SellerCommentModelSerializer, PostCreateModelSerializer, \
    CommentCreateModelSerializer, EditPostModelSerializer, CreateCategoryModelSerializer, CreateProductModelSerializer, \
    GetCategoriesModelSerializer, CommentEditModelSerializer, CategoryUpdateModelSerializer, \
    ProductUpdateModelSerializer


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
    permission_classes = [IsAuthenticated, IsCustomerPermission]
    queryset = Post.objects.all()
    serializer_class = AllPostForUserModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer=self.request.user)


@extend_schema(tags=['Customer'])
class PostDetailRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = PostDetailModelSerializer


@extend_schema(tags=['Seller'])
class SellerCommentAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSellerPermission]
    queryset = Comment.objects.all()
    serializer_class = SellerCommentModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(seller=self.request.user)


@extend_schema(tags=['Customer'], request=PostCreateModelSerializer)
class PostCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomerPermission]
    serializer_class = PostCreateModelSerializer
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema(tags=['Seller'])
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateModelSerializer
    permission_classes = [IsAuthenticated, IsSellerPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        post_id = self.kwargs['post_id']
        post = Post.objects.filter(id=post_id).first()
        context['post_id'] = post.id
        return context


@extend_schema(tags=['Customer'])
class PostUpdateAPIView(UpdateAPIView):
    permission_classes = [IsCustomerPermission]
    serializer_class = EditPostModelSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Customer'])
class PostDeleteAPIView(DestroyAPIView):
    permission_classes = [IsCustomerPermission]
    queryset = Post.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Seller'])
class CommentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsSellerPermission]
    queryset = Comment.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Seller'])
class AllPostsForSellerAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = AllPostForUserModelSerializer


@extend_schema(tags=['Admin'])
class AdminLoginApiView(TokenObtainPairView):
    permission_classes = [IsAdminPermission]


@extend_schema(tags=['Admin'])
class CategoryCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminPermission]
    queryset = Category.objects.all()
    serializer_class = CreateCategoryModelSerializer


@extend_schema(tags=["Admin"])
class GetCategoriesListAPIView(ListAPIView):
    serializer_class = CreateCategoryModelSerializer
    queryset = Category.objects.all()


@extend_schema(tags=["Admin"])
class CreateProductAPIView(CreateAPIView):
    serializer_class = CreateProductModelSerializer
    queryset = Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['category_id'] = self.kwargs.get('pk')
        return context


@extend_schema(tags=['Admin'])
class GetProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = GetCategoriesModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_id=self.kwargs.get('pk'))

@extend_schema(tags=['Seller'])
class EditCommentUpdateAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentEditModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['Admin'])
class CategoryUpdateAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['Admin'])
class DeleteCategoryDestroyAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Admin'])
class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductUpdateModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Admin'])
class ProductDestroyAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Admin'])
class AllProductsListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = GetCategoriesModelSerializer

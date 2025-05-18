from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User, Post, Comment, Category, CPU, MotherBoard, PowerUnit, Soket, GPU, RAM, Memory, Coller, \
    Keys, Monitor, Wifi, Accessor
from apps.permissions import IsSellerPermission, IsCustomerPermission, IsAdminPermission
from apps.serializers import RegisterModelSerializer, CustomTokenObtainPairSerializer, ProfileModelSerializer, \
    AllPostForUserModelSerializer, PostDetailModelSerializer, SellerCommentModelSerializer, PostCreateModelSerializer, \
    CommentCreateModelSerializer, EditPostModelSerializer, CreateCategoryModelSerializer, \
    CommentEditModelSerializer, CategoryUpdateModelSerializer, CPUModelSerializer, MotherBoardModelSerializer, \
    PowerUnitModelSerializer, PowerUnitPostSerializer, CPUCreateModelSerializer, \
    MotherBoardViewSetModelSerializer, SoketSerializer, GPUModelSerializer, RAMModelSerializer, MemoryModelSerializer, \
    CollerModelSerializer, KeysModelSerializer, MonitorModelSerializer, WifiModelSerializer, AccessorModelSerializer


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


# @extend_schema(tags=["Admin"])
# class CreateProductAPIView(CreateAPIView):
#     serializer_class = CreateProductModelSerializer
#     queryset = Product.objects.all()
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['category_id'] = self.kwargs.get('pk')
#         return context
#
#
# @extend_schema(tags=['Admin'])
# class GetProductListAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = GetCategoriesModelSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(category_id=self.kwargs.get('pk'))

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


# @extend_schema(tags=['Admin'])
# class ProductUpdateAPIView(UpdateAPIView):
#     serializer_class = ProductUpdateModelSerializer
#     queryset = Product.objects.all()
#     lookup_field = 'pk'
#
#
# @extend_schema(tags=['Admin'])
# class ProductDestroyAPIView(DestroyAPIView):
#     queryset = Product.objects.all()
#     lookup_field = 'pk'
#
#
# @extend_schema(tags=['Admin'])
# class AllProductsListAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = GetCategoriesModelSerializer


# @extend_schema(tags=['Customer'])
# class AllCategoryProductListAPIView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = AllCategoryAllProductModelSerializer

@extend_schema(tags=['Customer Last Updates'])
class CPUListAPIView(ListAPIView):
    queryset = CPU.objects.all()
    serializer_class = CPUModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = Category.objects.filter(id=self.kwargs['category_id']).first()
        return category.cpus


@extend_schema(tags=['Customer Last Updates'])
class MotherBoardListAPIView(ListAPIView):
    queryset = MotherBoard.objects.all()
    serializer_class = MotherBoardModelSerializer

    def get_queryset(self):
        cpu = CPU.objects.filter(id=self.kwargs['cpu_id']).first()
        soket = cpu.soket
        return super().get_queryset().filter(soket=soket)


# @extend_schema(tags=['Customer Last Updates'])
# class OtherListAPIView(ListAPIView):
#     queryset = Other.objects.all()
#     serializer_class = OtherModelSerializer
#
#     def get_queryset(self):
#         others = Other.objects.all()
#         return others

@extend_schema(tags=['Customer Last Updates'], request=PowerUnitPostSerializer)
@api_view(['POST'])
def power_unit_api_view(request):
    cpu_power = request.data['cpu_power']
    videocard_power = request.data['videocard_power']

    overall = cpu_power + videocard_power
    power_units = PowerUnit.objects.filter(power__gte=overall)
    if power_units:
        return Response(PowerUnitModelSerializer(power_units, many=True).data)
    return Response('Power Units not found')


@extend_schema(tags=['Admin Last Updates'])
class CPUAddCreateAPIView(CreateAPIView):
    serializer_class = CPUCreateModelSerializer


@extend_schema(tags=['Admin Last Updates'])
class CPUUpdateAPIView(UpdateAPIView):
    queryset = CPU.objects.all()
    lookup_field = 'pk'
    serializer_class = CPUCreateModelSerializer


@extend_schema(tags=['Admin Last Updates'])
class CPUDestroyAPIView(DestroyAPIView):
    queryset = CPU.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['Admin Last Updates'])
class MotherBoardViewSet(ModelViewSet):
    queryset = MotherBoard.objects.all()
    serializer_class = MotherBoardViewSetModelSerializer


@extend_schema(tags=['Admin Last Updates'])
class SoketViewSet(ModelViewSet):
    queryset = Soket.objects.all()
    serializer_class = SoketSerializer


# @extend_schema(tags=['Admin Last Updates'])
# class OtherViewSet(ModelViewSet):
#     queryset = Other.objects.all()
#     serializer_class = OtherModelSerializer

@extend_schema(tags=['Admin Last Updates'])
class PowerUnitViewSet(ModelViewSet):
    queryset = PowerUnit.objects.all()
    serializer_class = PowerUnitModelSerializer


@extend_schema(tags=['Admin Last Updates'])
class CPUModelViewSet(ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUCreateModelSerializer


# ======================= Second Update ===============

@extend_schema(tags=['Customer Last Updates'])
class AllGPUListAPIView(ListAPIView):
    queryset = GPU.objects.all()
    serializer_class = GPUModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_id=self.kwargs['category_id'])


@extend_schema(tags=['Customer Last Updates'])
class AllRamsListAPIView(ListAPIView):
    queryset = RAM.objects.all()
    serializer_class = RAMModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = Category.objects.filter(id=self.kwargs['category_id']).first()
        if category.name == Category.CategoryChoices.gaming:
            return queryset.filter(type=RAM.TypeChoices.ddr5)
        return queryset


@extend_schema(tags=['Customer Last Updates'])
class AllMemoryModelSerializer(ListAPIView):
    serializer_class = MemoryModelSerializer
    queryset = Memory.objects.all()


@extend_schema(tags=['Customer Last Updates'])
class CollerListAPIView(ListAPIView):
    serializer_class = CollerModelSerializer
    queryset = Coller.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_id=self.kwargs['category_id'])


@extend_schema(tags=['Customer Last Updates'])
class KeysListAPIView(ListAPIView):
    serializer_class = KeysModelSerializer
    queryset = Keys.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['category_id'])


@extend_schema(tags=['Customer Last Updates'])
class MonitorListAPIView(ListAPIView):
    serializer_class = MonitorModelSerializer
    queryset = Monitor.objects.all()


@extend_schema(tags=['Customer Last Updates'])
class WifiListAPIView(ListAPIView):
    serializer_class = WifiModelSerializer
    queryset = Wifi.objects.all()


@extend_schema(tags=['Customer Last Updates'])
class AccessorListAPIView(ListAPIView):
    serializer_class = AccessorModelSerializer
    queryset = Accessor.objects.all()


@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class GPUViewSet(ModelViewSet):
    serializer_class = GPUModelSerializer
    queryset = GPU.objects.all()


@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class RAMViewSet(ModelViewSet):
    serializer_class = RAMModelSerializer
    queryset = RAM.objects.all()

@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class MemoryViewSet(ModelViewSet):
    serializer_class = MemoryModelSerializer
    queryset = Memory.objects.all()


@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class CollerViewSet(ModelViewSet):
    serializer_class = CollerModelSerializer
    queryset = Coller.objects.all()

@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class KeysViewSet(ModelViewSet):
    serializer_class = KeysModelSerializer
    queryset = Keys.objects.all()

@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class MonitorViewSet(ModelViewSet):
    serializer_class = MonitorModelSerializer
    queryset = Monitor.objects.all()

@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class WifiViewSet(ModelViewSet):
    serializer_class = WifiModelSerializer
    queryset = Wifi.objects.all()

@extend_schema(tags=["Adminga yangi qo'shilgan narsalar"])
class AccessorViewSet(ModelViewSet):
    serializer_class = AccessorModelSerializer
    queryset = Accessor.objects.all()
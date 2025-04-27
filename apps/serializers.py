from django.contrib.auth.hashers import make_password
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import User, Post, Comment, Category, Product


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
    user = SerializerMethodField()
    text = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'phone_number', 'price', 'user']

    def get_text(self, obj):
        return obj.text[:100] if len(obj.text) >= 100 else obj.text

    def get_user(self, obj):
        return ProfileModelSerializer(obj.customer).data


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
        model = Comment
        fields = ['text']

    def validate(self, attrs):
        attrs['seller'] = self.context['request'].user
        attrs['post_id'] = self.context['post_id']
        return attrs


class EditPostModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'phone_number', 'price']


class CreateCategoryModelSerializer(ModelSerializer):
    email = CharField(write_only=True)

    class Meta:
        model = Category
        fields = ['id', "name", 'email']

    def validate(self, attrs):
        attrs.pop('email')
        return attrs


class CreateProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def validate(self, attrs):
        attrs['category_id'] = self.context.get('category_id')
        return attrs


class GetCategoriesModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']
        depth = 1


class CommentEditModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']


class CategoryUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']

        extra_kwargs = {
            'price': {'required': False},
            'name': {'required': False}
        }


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class AllCategoryAllProductModelSerializer(ModelSerializer):
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name','products']

    def get_products(self, obj):
        return ProductModelSerializer(obj.products, many=True).data

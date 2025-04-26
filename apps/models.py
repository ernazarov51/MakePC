from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import EmailField, CharField, BooleanField, DateField, ImageField, Model, ForeignKey, CASCADE, \
    DecimalField, TextField


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        seller = 'seller', 'seller'
        customer = 'customer', 'Customer'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    email = EmailField("email address", unique=True)
    role=CharField(max_length=255,choices=Roles.choices)

class Category(Model):
    name=CharField(max_length=255,unique=True)

class Product(Model):
    category=ForeignKey('apps.Category',on_delete=CASCADE,related_name='products')
    name=CharField(max_length=255)
    price=DecimalField(max_digits=10, decimal_places=2)

class Post(Model):
    text=TextField()
    price=DecimalField(max_digits=10, decimal_places=2)
    phone_number=CharField(max_length=20)
    customer=ForeignKey('apps.User',on_delete=CASCADE,related_name='posts')

class Comment(Model):
    text=TextField()
    post=ForeignKey('apps.Post',on_delete=CASCADE,related_name='comments')
    seller=ForeignKey('apps.User',on_delete=CASCADE,related_name='comments')


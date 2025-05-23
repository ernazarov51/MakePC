from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import EmailField, CharField, BooleanField, DateField, ImageField, Model, ForeignKey, CASCADE, \
    DecimalField, TextField, TextChoices, SmallIntegerField


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
    role = CharField(max_length=255, choices=Roles.choices)


class Category(Model):
    class CategoryChoices(TextChoices):
        gaming = 'gaming', 'GAMING'
        office = 'office', 'OFFICE'
        montage = 'montage', 'MONTAGE'

    name = CharField(max_length=255, choices=CategoryChoices.choices)

    def __str__(self):
        return self.name


class Soket(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class CPU(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    soket = ForeignKey('apps.Soket', CASCADE, related_name='cpus')
    power = SmallIntegerField()
    category = ForeignKey('apps.Category', CASCADE, related_name='cpus')

    def __str__(self):
        return self.name


class MotherBoard(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    soket = ForeignKey('apps.Soket', CASCADE, related_name='motherboards')

    def __str__(self):
        return self.name


class PowerUnit(Model):
    name = CharField(max_length=255)
    power = SmallIntegerField()
    price = SmallIntegerField()

    def __str__(self):
        return self.name


class Post(Model):
    text = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    phone_number = CharField(max_length=20)
    customer = ForeignKey('apps.User', on_delete=CASCADE, related_name='posts')


class Comment(Model):
    text = TextField()
    post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='comments')
    seller = ForeignKey('apps.User', on_delete=CASCADE, related_name='comments')


class CategoryP(Model):
    image = ImageField(upload_to='apps/images/category')
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(Model):
    image = ImageField(upload_to='apps/images/product')
    name = CharField(max_length=255)
    text = TextField()
    price = SmallIntegerField()
    category = ForeignKey('apps.CategoryP', on_delete=CASCADE, related_name='products')


class GPU(Model):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='gpus')
    price = SmallIntegerField()
    power = SmallIntegerField(null=True, blank=True)


class RAM(Model):
    class TypeChoices(TextChoices):
        ddr4 = 'ddr4', 'DDR4'
        ddr5 = 'ddr5', 'DDR5'

    name = CharField(max_length=255)
    price = SmallIntegerField()
    type = CharField(max_length=10, choices=TypeChoices.choices)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='rams')
    power = SmallIntegerField(null=True, blank=True)


class Memory(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()


class Coller(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='collers')


class Keys(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='keys')


class Monitor(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()
    pixel = CharField(max_length=255)


class Wifi(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()


class Accessor(Model):
    name = CharField(max_length=255)
    price = SmallIntegerField()

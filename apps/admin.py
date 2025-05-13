from django.contrib import admin

from apps.models import Category, CPU, Soket, MotherBoard, Other, PowerUnit

# Register your models here.
admin.site.register(Category)
admin.site.register(CPU)
admin.site.register(Soket)
admin.site.register(MotherBoard)
admin.site.register(Other)
admin.site.register(PowerUnit)
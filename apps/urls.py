from django.urls import path

from apps.views import RegisterCreateAPIView

urlpatterns=[
    path('register/',RegisterCreateAPIView.as_view(),name='register'),
    path('profile/',RegisterCreateAPIView.as_view(),name='register')
]
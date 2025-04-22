from django.urls import path

from apps.views import RegisterCreateAPIView, user_profile_api_view

urlpatterns=[
    path('register/',RegisterCreateAPIView.as_view(),name='register'),
    path('profile/',user_profile_api_view,name='register')
]
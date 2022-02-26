from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('auth/login/', ObtainAuthToken)
]

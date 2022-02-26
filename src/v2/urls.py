from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import renderers

ObtainAuthToken.renderer_classes = (renderers.JSONRenderer,
                                    renderers.BrowsableAPIRenderer)

urlpatterns = [
    path('auth/login/', ObtainAuthToken.as_view())
]

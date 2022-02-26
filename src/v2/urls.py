from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from . import views

ObtainAuthToken.renderer_classes = (renderers.JSONRenderer,
                                    renderers.BrowsableAPIRenderer)

router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'block', views.TextBlockViewSet)
router.register(r'permission/block', views.PermissionBlockViewSet)

urlpatterns = router.urls + [
    path('auth/login/', ObtainAuthToken.as_view()),
]

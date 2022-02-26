from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGET, IsPOST, IsPATCH, IsDELETE

from . import models
from . import serializers


class UserViewSet(GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    permission_classes = [
        (IsPOST & ~IsAuthenticated) |
        (IsGET & IsAuthenticated)
    ]

    def list(self, request):
        """Return authenticated user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

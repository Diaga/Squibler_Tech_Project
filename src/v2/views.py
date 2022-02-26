from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGET, IsPOST, IsPATCH, IsDELETE, IsOWNER, IsEDITOR, \
    IsVIEW

from . import models
from . import serializers


class UserViewSet(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin):
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


class TextBlockViewSet(GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = models.TextBlock.objects.all()
    serializer_class = serializers.TextBlockSerializer

    permission_classes = [
        IsAuthenticated,
        (IsPOST & (IsOWNER | IsEDITOR)) |
        (IsGET & (IsOWNER | IsEDITOR | IsVIEW)) |
        (IsPATCH & (IsOWNER | IsEDITOR)) |
        (IsDELETE & (IsOWNER | IsEDITOR))
    ]

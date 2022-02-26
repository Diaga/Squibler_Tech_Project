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


class PermissionBlockViewSet(GenericViewSet,
                             mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin):
    queryset = models.PermissionBlock.objects.all()
    serializer_class = serializers.PermissionBlockSerializer

    permission_classes = [
        IsAuthenticated,
        IsOWNER
    ]

    def get_queryset(self):
        queryset = super(PermissionBlockViewSet, self).get_queryset()

        block_id = self.request.query_params.get('block', None)
        if block_id is not None:
            return queryset.filter(block__id=block_id).all()

        return models.PermissionBlock.objects.none() \
            if self.request.method == 'GET' else queryset

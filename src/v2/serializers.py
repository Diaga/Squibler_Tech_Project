from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email')


class TextBlockSerializer(ModelSerializer):
    class Meta:
        model = models.TextBlock
        fields = ('id', 'title', 'text', 'parent', 'children')


class PermissionBlock(ModelSerializer):
    class Meta:
        model = models.PermissionBlock
        fields = ('id', 'permission', 'block', 'user')

from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TextBlockSerializer(ModelSerializer):
    class Meta:
        model = models.TextBlock
        fields = ('id', 'title', 'text', 'parent', 'children')
        extra_kwargs = {
            'children': {'required': False}
        }

    def create(self, validated_data):
        instance = super().create(validated_data)

        if instance.parent is None:
            models.PermissionBlock.objects.create(
                block=instance,
                user=self.context['request'].user,
                permission=models.PermissionBlock.PermissionEnum.OWNER
            )

        return instance


class PermissionBlockSerializer(ModelSerializer):
    class Meta:
        model = models.PermissionBlock
        fields = ('id', 'permission', 'block', 'user')

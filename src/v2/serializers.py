from rest_framework.serializers import ModelSerializer, ValidationError, \
    CharField
import diff_match_patch as dmp_module
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TextBlockSerializer(ModelSerializer):
    text_diff = CharField(required=False, write_only=True)

    class Meta:
        model = models.TextBlock
        fields = ('id', 'title', 'text', 'parent', 'children',
                  'text_diff')
        extra_kwargs = {
            'children': {'required': False}
        }

    def create(self, validated_data):
        instance = super(TextBlockSerializer, self).create(validated_data)

        if instance.parent is None:
            models.PermissionBlock.objects.create(
                block=instance,
                user=self.context['request'].user,
                permission=models.PermissionBlock.PermissionEnum.OWNER
            )

        return instance

    def update(self, instance, validated_data):
        instance = super(TextBlockSerializer, self).update(instance,
                                                           validated_data)

        text_diff = validated_data.get('text_diff', None)
        if text_diff is not None:
            dmp = dmp_module.diff_match_patch()
            instance.text, _ = dmp.patch_apply(dmp.patch_fromText(text_diff),
                                               instance.text)
            instance.save()

        return instance


class PermissionBlockSerializer(ModelSerializer):

    def validate_block(self, value):
        if self.instance and value.id != self.instance.block.id:
            raise ValidationError('block is immutable once set')
        return value

    def validate_user(self, value):
        if self.instance and value.id != self.instance.user.id:
            raise ValidationError('user is immutable once set')
        return value

    class Meta:
        model = models.PermissionBlock
        fields = ('id', 'permission', 'block', 'user')

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField(unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        app_label = 'v2'
        default_related_name = 'users'

    def __str__(self):
        return self.email


class TextBlockManager(models.Manager):

    @staticmethod
    def find_root(block_id):
        """Recursively finds the root of the block"""
        return TextBlock.objects.raw('''
                WITH RECURSIVE block(id, parent) AS (
                      SELECT id, parent 
                      FROM v2_textblock
                      WHERE id = %s
                    UNION ALL
                      SELECT tb.id, tb.parent
                      FROM v2_textblock AS tb, block AS b
                      WHERE tb.id = b.parent
                    )
                SELECT * FROM v2_textblock
            ''', [block_id, ])


class TextBlock(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=255, default='Untitled')
    text = models.TextField(blank=True)

    parent = models.ForeignKey('TextBlock', on_delete=models.CASCADE,
                               null=True)

    objects = TextBlockManager()

    class Meta:
        app_label = 'v2'
        default_related_name = 'children'

    def __str__(self):
        return self.title


class PermissionBlock(models.Model):
    class PermissionEnum(models.TextChoices):
        VIEW = 'View', 'View'
        EDITOR = 'Editor', 'Editor'
        OWNER = 'Owner', 'Owner'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    permission = models.CharField(choices=PermissionEnum.choices,
                                  max_length=255)

    block = models.ForeignKey(TextBlock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def parent(self):
        """For compatibility with TextBlock permissions"""
        return self.block

    class Meta:
        app_label = 'v2'
        default_related_name = 'permission_blocks'

    def __str__(self):
        return f'{self.permission} - {self.block} - {self.user}'

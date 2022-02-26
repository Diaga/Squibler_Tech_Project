from rest_framework.permissions import BasePermission
from . import models


class IsPOST(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class IsGET(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'GET'


class IsPATCH(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'PATCH'


class IsDELETE(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'DELETE'


class IsOWNER(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            parent_id = request.data.get('parent', None)
            if parent_id is not None:
                root = models.TextBlock.objects.find_root(parent_id)[0]
                return root.permission_blocks.filter(
                    user=request.user,
                    permission=models.PermissionBlock.PermissionEnum.OWNER
                ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        root = obj if obj.parent is None else \
            models.TextBlock.objects.find_root(obj.parent.id)[0]

        return root.permission_blocks.filter(
            user=request.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        ).exists()


class IsEDITOR(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            parent_id = request.data.get('parent', None)
            if parent_id is not None:
                root = models.TextBlock.objects.find_root(parent_id)[0]
                return root.permission_blocks.filter(
                    user=request.user,
                    permission=models.PermissionBlock.PermissionEnum.EDITOR
                ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        root = obj if obj.parent is None else \
            models.TextBlock.objects.find_root(obj.parent.id)[0]

        return root.permission_blocks.filter(
            user=request.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        ).exists()


class IsVIEW(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            parent_id = request.data.get('parent', None)
            if parent_id is not None:
                root = models.TextBlock.objects.find_root(parent_id)[0]
                return root.permission_blocks.filter(
                    user=request.user,
                    permission=models.PermissionBlock.PermissionEnum.VIEW
                ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        root = obj if obj.parent is None else \
            models.TextBlock.objects.find_root(obj.parent.id)[0]

        return root.permission_blocks.filter(
            user=request.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        ).exists()

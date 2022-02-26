from rest_framework.permissions import BasePermission
from . import models


class IsPOST(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsGET(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'GET'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsPATCH(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'PATCH'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsDELETE(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'DELETE'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


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
            models.TextBlock.objects.find_root(str(obj.parent.id))[0]

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
            models.TextBlock.objects.find_root(str(obj.parent.id))[0]

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
            models.TextBlock.objects.find_root(str(obj.parent.id))[0]

        return root.permission_blocks.filter(
            user=request.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        ).exists()

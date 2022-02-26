from rest_framework.permissions import BasePermission


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

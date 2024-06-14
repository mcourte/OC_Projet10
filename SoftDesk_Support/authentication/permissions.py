from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj == request.user


class AllowAnonymousAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

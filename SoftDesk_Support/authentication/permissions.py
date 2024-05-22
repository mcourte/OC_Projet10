from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission personnalisée pour permettre uniquement aux administrateurs de voir la liste des utilisateurs.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsUser(BasePermission):
    """
    Permission personnalisée pour permettre aux utilisateurs de modifier leur propre profil.
    """

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj == request.user


class AllowAnonymousAccess(BasePermission):
    """
    Permission pour refuser l'accès aux utilisateurs anonymes.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

from rest_framework.permissions import BasePermission


class AllowAnonymousAccess(BasePermission):
    """
    Permission permettant l'accès anonyme.

    Cette permission autorise toutes les requêtes, quel que soit l'utilisateur.
    """

    def has_permission(self, request, view):
        """
        Détermine si la permission est accordée.
        """
        return True


class IsAdmin(BasePermission):
    """
    Permission réservée aux administrateurs.
    """

    def has_permission(self, request, view):
        """
        Détermine si la permission est accordée.
        """
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsUser(BasePermission):
    """
    Permission réservée à l'utilisateur concerné.

    Cette permission est accordée si l'objet de la requête appartient à l'utilisateur authentifié.
    """

    def has_object_permission(self, request, view, obj):
        """
        Détermine si la permission est accordée pour l'objet spécifique.
        """
        return request.user and request.user.is_authenticated and obj == request.user

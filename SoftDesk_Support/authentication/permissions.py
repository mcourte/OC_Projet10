from rest_framework.permissions import BasePermission


class AllowAnonymousAccess(BasePermission):
    """
    Permission permettant l'accès anonyme.

    Cette permission autorise toutes les requêtes, quel que soit l'utilisateur.
    """

    def has_permission(self, request, view):
        """
        Détermine si la permission est accordée.

        Args:
            request (HttpRequest): La requête en cours.
            view (View): La vue en cours.

        Returns:
            bool: Toujours True, ce qui signifie que l'accès est toujours autorisé.
        """
        return True


class IsAdmin(BasePermission):
    """
    Permission réservée aux administrateurs.

    Cette permission n'est accordée qu'aux utilisateurs authentifiés ayant le statut de staff.
    """

    def has_permission(self, request, view):
        """
        Détermine si la permission est accordée.

        Args:
            request (HttpRequest): La requête en cours.
            view (View): La vue en cours.

        Returns:
            bool: True si l'utilisateur est authentifié et est staff, sinon False.
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

        Args:
            request (HttpRequest): La requête en cours.
            view (View): La vue en cours.
            obj (Model): L'objet à vérifier.

        Returns:
            bool: True si l'utilisateur est authentifié et est le propriétaire de l'objet, sinon False.
        """
        return request.user and request.user.is_authenticated and obj == request.user

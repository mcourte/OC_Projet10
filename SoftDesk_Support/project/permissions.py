from rest_framework import permissions
from project.models import Project, Issue, Comment


class IsAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est l'auteur du projet, du problème ou du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return request.user == obj.author
        elif isinstance(obj, Issue):
            return request.user == obj.author
        elif isinstance(obj, Comment):
            return request.user == obj.author
        return False


class IsContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est un contributeur du projet ou l'auteur du projet du problème ou du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return request.user == obj.author
        elif isinstance(obj, Issue):
            return self._is_contributor_or_author(request.user, obj.project)
        elif isinstance(obj, Comment):
            return self._is_contributor_or_author(request.user, obj.issue.project)
        return False

    def _is_contributor_or_author(self, user, project):
        return user == project.author or user in project.contributors.all()


class AllowAnonymousAccess(permissions.BasePermission):
    """
    Permission pour refuser l'accès aux utilisateurs non authentifiés.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour permettre un accès limité aux utilisateurs authentifiés qui ne sont ni auteurs ni contributeurs.
    """

    def has_object_permission(self, request, view, obj):
        # Ici, vous pouvez définir les permissions d'accès limité
        # Par exemple, permettre uniquement la lecture des commentaires
        return request.method in permissions.SAFE_METHODS

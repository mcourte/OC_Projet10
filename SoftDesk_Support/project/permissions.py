from rest_framework import permissions
from project.models import Project, Issue, Comment


class IsAuthor(permissions.BasePermission):
    """
    Permission pour permettre l'accès si l'utilisateur est l'auteur de l'objet.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            return request.user == obj.author
        return False


class IsContributor(permissions.BasePermission):
    """
    Permission pour permettre l'accès si l'utilisateur est un contributeur du projet associé.
    """
    def _get_project_from_obj(self, obj):
        if isinstance(obj, Project):
            return obj
        elif isinstance(obj, Issue):
            return obj.project
        elif isinstance(obj, Comment):
            return obj.issue.project
        return None

    def has_object_permission(self, request, view, obj):
        project = self._get_project_from_obj(obj)
        if project and project.contributors.filter(id=request.user.id).exists():
            return True
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour permettre l'accès uniquement aux utilisateurs authentifiés.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

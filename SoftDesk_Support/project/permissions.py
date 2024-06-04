from rest_framework import permissions
from project.models import Project, Issue, Comment


class IsAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est l'auteur du projet, du problème ou du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est un contributeur du projet ou l'auteur du projet du problème ou du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        project = self._get_project_from_obj(Project)
        return project and (request.user == project.author or request.user in project.contributors.all())

    def _get_project_from_obj(self, obj):
        if isinstance(obj, Project):
            return obj
        if isinstance(obj, Issue):
            return obj.project
        if isinstance(obj, Comment):
            return obj.issue.project
        return None


class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour permettre l'accès uniquement aux utilisateurs authentifiés.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

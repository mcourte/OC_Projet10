from rest_framework import permissions
from project.models import Project, Issue, Comment


class IsProjectContributorOrAuthor(permissions.BasePermission):
    """
    Permission pour permettre uniquement aux contributeurs d'un projet ou à l'auteur d'y accéder.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return request.user in obj.contributors.all() or request.user == obj.author
        return False


class IsProjectAuthor(permissions.BasePermission):
    """
    Permission pour permettre uniquement à l'auteur d'un projet de le modifier ou de le supprimer.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return request.user == obj.author
        return False


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour permettre uniquement aux contributeurs d'un projet d'accéder aux fonctionnalités spécifiques.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return request.user in obj.contributors.all()
        return False


class IsIssueAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est l'auteur de l'issue.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Issue):
            return request.user == obj.author
        return False


class IsIssueContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est un contributeur du projet de l'issue.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Issue):
            return request.user in obj.project.contributors.all() or request.user == obj.project.author
        return False


class IsCommentAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est l'auteur du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Comment):
            return request.user == obj.author
        return False


class IsCommentContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur est un contributeur du projet du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Comment):
            return request.user in obj.issue.project.contributors.all() or request.user == obj.issue.project.author
        return False


class AllowAnonymousAccess(permissions.BasePermission):
    """
    Permission pour refuser l'accès aux utilisateurs anonymes.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

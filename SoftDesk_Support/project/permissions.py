from rest_framework import permissions
from project.models import Project, Issue, Comment, Contributor


class IsAuthorOrContributor(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès si l'utilisateur est soit l'auteur,
    soit un contributeur, soit authentifié avec certaines restrictions.
    """

    def _get_project_from_obj(self, obj):
        if isinstance(obj, Project):
            return obj
        elif isinstance(obj, Issue):
            return obj.project
        elif isinstance(obj, Comment):
            return obj.issue.project
        elif isinstance(obj, Contributor):
            return obj.project
        return None

    def has_object_permission(self, request, view, obj):
        project = self._get_project_from_obj(obj)

        # Vérifiez si l'objet a un champ 'author'
        if hasattr(obj, 'author'):
            # Vérifiez si l'utilisateur est l'auteur de l'objet
            if request.user == obj.author:
                return True

        # Si l'objet n'a pas de champ 'author', vérifiez si l'utilisateur est un contributeur du projet
        elif project and request.user in project.contributors.all():
            # Autoriser les méthodes sûres (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return True

        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour permettre l'accès uniquement aux utilisateurs authentifiés.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

from rest_framework import permissions
from project.models import Project, Issue, Comment


class IsAuthorOrContributor(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès si l'utilisateur est soit l'auteur,
    soit un contributeur, soit authentifié avec certaines restrictions.
    """

    def _get_project_from_obj(self, obj):
        # Implémentez cette méthode pour extraire le projet de l'objet.
        if isinstance(obj, Project):
            return obj
        elif isinstance(obj, Issue):
            return obj.project
        elif isinstance(obj, Comment):
            return obj.issue.project
        return None

    def has_object_permission(self, request, view, obj):
        # Vérifiez si l'utilisateur est l'auteur
        if request.user == obj.author:
            return True

        # Vérifiez si l'utilisateur est un contributeur
        project = self._get_project_from_obj(obj)
        if project and request.user in project.contributors.all():
            # Les contributeurs peuvent effectuer les opérations GET et POST
            if request.method in permissions.SAFE_METHODS + ['POST']:
                return True

        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour permettre l'accès uniquement aux utilisateurs authentifiés.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

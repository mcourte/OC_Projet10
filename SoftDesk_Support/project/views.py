from rest_framework import viewsets
from .models import Project, Issue, Comment
from serializers import (
        ProjectSerializer,
        ProjectListSerializer,
        ContributorSerializer,
        IssueSerializer,
        CommentSerializer,
    )
from .permissions import (
    IsAuthor,
    IsContributor,
    AllowAnonymousAccess,
    IsAuthenticated
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Projet.

    Create : Créer un projet.
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """

    serializer_mapping = {
        "list": ProjectListSerializer,
        "retrieve": ProjectSerializer,
        "create": ProjectSerializer,
        "update": ProjectSerializer,
        "partial_update": ProjectSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_queryset(self):
        return Project.objects.filter(active=True)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CONTRIBUTOR.

    Create : Créer un Contributor.
    Read : Visualiser un Contributor.
    Update : Modifier un Contributor.
    Delete : Supprimer un Contributor.
    """

    serializer_class = ContributorSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Issue.

    Create : Créer une Issue.
    Read : Visualiser une Issue.
    Update : Modifier une Issue.
    Delete : Supprimer une Issue.
    """

    serializer_mapping = {
        "list": IssueSerializer,
        "retrieve": IssueSerializer,
        "create": IssueSerializer,
        "update": IssueSerializer,
        "partial_update": IssueSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_queryset(self):
        queryset = Issue.objects.filter(active=True)
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Comment.

    Create : Créer un Comment.
    Read : Visualiser un Comment.
    Update : Modifier un Comment.
    Delete : Supprimer un Comment.
    """

    serializer_mapping = {
        "list": CommentSerializer,
        "retrieve": CommentSerializer,
        "create": CommentSerializer,
        "update": CommentSerializer,
        "partial_update": CommentSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_queryset(self):
        queryset = Comment.objects.filter(active=True)
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset

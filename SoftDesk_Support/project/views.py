from rest_framework import viewsets
from .models import Project, Issue, Comment
from project.SerializerMixin import SerializerMixin
from serializers import (
        ProjectCreateSerializer,
        ProjectListSerializer,
        ProjectDetailSerializer,
        ProjectUpdateSerializer,
        ContributorSerializer,
        IssueCreateSerializer,
        IssueDetailSerializer,
        IssueListSerializer,
        CommentCreateSerializer,
        CommentListSerializer,
        CommentDetailSerializer,
    )
from .permissions import (
    IsProjectContributorOrAuthor,
    IsProjectAuthor,
    IsProjectContributor,
    IsIssueAuthor,
    IsIssueContributor,
    IsCommentAuthor,
    IsCommentContributor,
    AllowAnonymousAccess
)


class ProjectViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    Permet de gérer les opérations CRUD sur le modèle Projet.

    Create : Créer un projet.
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """

    serializer_mapping = {
        "list": ProjectListSerializer,
        "retrieve": ProjectDetailSerializer,
        "create": ProjectCreateSerializer,
        "update": ProjectUpdateSerializer,
        "partial_update": ProjectUpdateSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_queryset(self):
        return Project.objects.filter(active=True)

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsProjectContributorOrAuthor]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = [IsProjectContributor]

        return [permission() for permission in permission_classes]


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CONTRIBUTOR.

    Create : Créer un Contributor.
    Read : Visualiser un Contributor.
    Update : Modifier un Contributor.
    Delete : Supprimer un Contributor.
    """

    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsProjectContributorOrAuthor]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsProjectContributorOrAuthor]
        else:
            permission_classes = [IsProjectContributorOrAuthor]

        return [permission() for permission in permission_classes]


class IssueViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    Permet de gérer les opérations CRUD sur le modèle Issue.

    Create : Créer une Issue.
    Read : Visualiser une Issue.
    Update : Modifier une Issue.
    Delete : Supprimer une Issue.
    """

    serializer_mapping = {
        "list": IssueListSerializer,
        "retrieve": IssueDetailSerializer,
        "create": IssueCreateSerializer,
        "update": IssueDetailSerializer,
        "partial_update": IssueDetailSerializer,
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

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsProjectContributorOrAuthor]
        elif self.action in ["activate", "deactivate"]:
            permission_classes = [IsProjectAuthor]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsIssueAuthor]
        else:
            permission_classes = [IsIssueContributor]

        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    Permet de gérer les opérations CRUD sur le modèle Comment.

    Create : Créer un Comment.
    Read : Visualiser un Comment.
    Update : Modifier un Comment.
    Delete : Supprimer un Comment.
    """

    serializer_mapping = {
        "list": CommentListSerializer,
        "retrieve": CommentDetailSerializer,
        "create": CommentCreateSerializer,
        "update": CommentDetailSerializer,
        "partial_update": CommentDetailSerializer,
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

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsIssueContributor]
        elif self.action in ["activate", "deactivate"]:
            permission_classes = [IsProjectAuthor, IsIssueAuthor]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsCommentAuthor]
        else:
            permission_classes = [IsCommentContributor]

        return [permission() for permission in permission_classes]

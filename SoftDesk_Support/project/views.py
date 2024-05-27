from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .models import Project, Issue, Comment
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import (
        ProjectSerializer,
        ProjectListSerializer,
        ContributorSerializer,
        IssueSerializer,
        CommentSerializer,
    )
from .permissions import (
    IsAuthor,
    IsContributor,
    IsAuthenticated
)
from authentication.permissions import AllowAnonymousAccess


class LoginView(viewsets.ModelViewSet):
    """Permet à toute personne accédant à l'application
    de se connecter ou de créer un compte.
    """

    permission_classes = [AllowAnonymousAccess]


class HomeView(viewsets.ModelViewSet):
    """Permet à toute personne identifié, de voir la liste de tous les Projets
    de voir la liste des projets où il est Contributeur, de créer un Projet."""

    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Projet.

    Create : Créer un projet.
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """

    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié pour chaque action de la vue.
        """
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        """
        Retourne le queryset filtré pour les projets actifs.
        """
        return Project.objects.filter(active=True)

    def perform_create(self, serializer):
        """
        Crée un nouveau Projet et l'associe à l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)
        return Response(
            {"message": "Le Projet a été créé avec succès."},
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        """
        Met à jour un Projet si l'utilisateur connecté est l'auteur.
        """
        instance = self.get_object()
        if self.request.user == instance.author:
            serializer.save()
            return Response(
                {"message": "Le Projet a été modifié avec succès."},
                status=status.HTTP_200_OK
            )
        raise ValidationError("Seul l'auteur du Projet peut le modifier.")

    def perform_destroy(self, instance):
        """
        Supprime un Projet si l'utilisateur connecté est l'auteur.
        """
        if self.request.user == instance.author:
            instance.delete()
            return Response(
                {"message": "Le Projet a été supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        raise ValidationError("Seul l'auteur du Projet peut le supprimer.")


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Contributor.

    Create : Créer un Contributor.
    Read : Visualiser un Contributor.
    Update : Modifier un Contributor.
    Delete : Supprimer un Contributor.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor]

    @property
    def project(self):
        """
        Récupère le projet associé à l'utilisateur connecté en préchargeant les contributeurs.
        """
        if not hasattr(self, '_project'):
            self._project = get_object_or_404(
                Project.objects.all().prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project

    def get_queryset(self):
        """
        Retourne le queryset des contributeurs du projet associé, ordonné par date de création.
        """
        return self.project.contributors.all().order_by("created_time")

    def get_serializer_class(self):
        """
        Retourne la classe de sérialiseur en fonction de l'action.
        """
        if self.action == "retrieve":
            return ContributorSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        Ajoute l'utilisateur validé des données du sérialiseur aux contributeurs du projet.
        """
        if self.request.user != self.project.author:
            raise ValidationError("Seul l'auteur du projet peut ajouter des contributeurs.")
        self.project.contributors.add(serializer.validated_data["user"])
        return Response(
            {"message": "Le Contributeur a été ajouté avec succès."},
            status=status.HTTP_201_CREATED
        )

    def perform_destroy(self, instance):
        """
        Supprimer un Contributor du Project.
        """
        if self.request.user == self.project.author:
            self.project.contributors.remove(instance)

            return Response(
                {"message": "Le Contributeur a été supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            raise ValidationError(
                "Seul l'auteur du Projet peuvent supprimer des Contributeurs."
            )


class IssueViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Issue.

    Create : Créer une Issue.
    Read : Visualiser une Issue.
    Update : Modifier une Issue.
    Delete : Supprimer une Issue.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Retourne le queryset filtré pour les issues actives.
        """
        queryset = Issue.objects.filter(active=True)
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    @property
    def issue(self):
        """
        Récupère les issues liées au projet.
        """
        if self._issue is None:
            self._issue = Issue.objects.filter(
                project_id=self.kwargs["project_pk"]
            )

        return self._issue

    def perform_create(self, serializer):
        """
        Crée une nouvelle Issue et l'associe à l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)
        return Response(
            {"message": "Le projet a été créé avec succès."},
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        """
        Met à jour une Issue si l'utilisateur connecté est l'auteur.
        """
        instance = self.get_object()
        if self.request.user == instance.author:
            serializer.save()
            return Response(
                {"message": "L'Issue a été modifiée avec succès."},
                status=status.HTTP_200_OK
            )
        raise ValidationError("Seul l'auteur de l'issue peut la modifier.")

    def perform_destroy(self, instance):
        """
        Supprime une Issue si l'utilisateur connecté est l'auteur.
        """
        if self.request.user == instance.author:
            instance.delete()
            return Response(
                {"message": "L'Issue a été supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        raise ValidationError("Seul l'auteur de l'issue peut la supprimer.")


class CommentViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Comment.

    Create : Créer un Comment.
    Read : Visualiser un Comment.
    Update : Modifier un Comment.
    Delete : Supprimer un Comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Retourne le queryset filtré pour les commentaires actifs.
        """
        queryset = Comment.objects.filter(active=True)
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset

    @property
    def comment(self):
        """
        Récupère les commentaires liés à l'issue spécifiée.
        """
        if self._comment is None:
            self._comment = Comment.objects.filter(
                issue_id=self.kwargs["issue_pk"]
            )

        return self._comment

    def perform_create(self, serializer):
        """
        Crée un nouveau Comment et l'associe à l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)
        return Response(
            {"message": "Le projet a été créé avec succès."},
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        """
        Met à jour un Comment si l'utilisateur connecté est l'auteur.
        """
        instance = self.get_object()
        if self.request.user == instance.author:
            serializer.save()
            return Response(
                {"message": "L'issue a été modifiée avec succès."},
                status=status.HTTP_200_OK
            )
        raise ValidationError("Seul l'auteur de l'issue peut la modifier.")

    def perform_destroy(self, instance):
        """
        Supprime un Comment si l'utilisateur connecté est l'auteur.
        """
        if self.request.user == instance.author:
            instance.delete()
            return Response(
                {"message": "Le Comment a été supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        raise ValidationError("Seul l'auteur du Comment peut le supprimer.")

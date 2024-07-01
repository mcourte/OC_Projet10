from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    ProjectCreateUpdateSerializer,
    ProjectListSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .permissions import IsAuthor, IsContributor, IsAuthenticated
from authentication.permissions import IsAdmin


class ProjectListViewSet(viewsets.ModelViewSet):
    """
    Permet de voir la liste des Projets existants et d'en créer un nouveau.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all().order_by('-created_time')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer  # Fallback serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Project.
    Create : Créer un projet.
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """
    permission_classes = [IsAuthor | IsContributor | IsAdmin]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message": "Le projet a été créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            serializer = ProjectCreateUpdateSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Le projet a été modifié avec succès."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("Seul l'auteur du Projet peut le modifier.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            return Response({"message": "Le projet a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("Seul l'auteur du Projet peut le supprimer.")


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Gère les contributeurs pour un projet spécifique.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor | IsContributor | IsAdmin]
    lookup_field = 'contributor_id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, project_id=project_id)
        serializer.save(project=project)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, project_id=project_id)

        if request.user != project.author:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.project.author:
            instance.delete()
            return Response({"message": "Le contributeur a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("Seul l'auteur du projet peut supprimer des contributeurs.")


class IssueViewSet(viewsets.ModelViewSet):
    """
    Gère les opérations CRUD sur le modèle Issue.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthor | IsContributor]
    lookup_field = 'issue_id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Issue.objects.filter(project_id=project_id)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, project_id=project_id)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, project=project)
            return Response({"message": "L'Issue a été créée avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "L'Issue a été modifiée avec succès."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("Seul l'auteur de l'issue peut la modifier.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            return Response({"message": "L'Issue a été supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("Seul l'auteur de l'issue peut la supprimer.")


class CommentViewSet(viewsets.ModelViewSet):
    """
    Gère les opérations CRUD sur le modèle Comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        return self.queryset.filter(issue_id=issue_id)

    def create(self, request, *args, **kwargs):
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, issue_id=issue_id)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, issue=issue)
            return Response({"message": "Le commentaire a été créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Le commentaire a été modifié avec succès."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("Seul l'auteur du commentaire peut le modifier.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            return Response({"message": "Le commentaire a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("Seul l'auteur du commentaire peut le supprimer.")

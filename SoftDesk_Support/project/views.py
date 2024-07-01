from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
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
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return redirect('projects')
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
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')

        if action == 'update':
            instance = self.get_object()
            if request.user == instance.author:
                serializer = ProjectCreateUpdateSerializer
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "Le projet a été modifié avec succès."},
                        status=status.HTTP_200_OK
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise ValidationError("Seul l'auteur du Projet peut le modifier.")

        elif action == 'destroy':
            instance = self.get_object()
            if request.user == instance.author:
                instance.delete()
                return redirect('projects')
            else:
                raise ValidationError("Seul l'auteur du Projet peut le supprimer.")

        else:
            raise ValidationError("Action non valide.")


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor | IsContributor | IsAdmin]
    lookup_field = 'contributor_id'

    def get_project(self):
        project_id = self.kwargs['project_id']
        return get_object_or_404(Project, project_id=project_id)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project__project_id=project_id)

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')
        project = self.get_project()

        if action == 'create':
            if not request.user.is_authenticated:
                return Response({"detail": "Vous devez être connecté pour effectuer cette action."},
                                status=status.HTTP_401_UNAUTHORIZED)

            if request.user != project.author:
                return Response({"detail": "Seul l'auteur du projet peut ajouter des contributeurs."},
                                status=status.HTTP_403_FORBIDDEN)

            # Ajoutez 'project' aux données envoyées
            request.data['project'] = project.id

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Action non prise en charge."},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            # Redirection vers une autre URL après suppression
            return redirect('projects')
        else:
            return Response(
                {"message": "Seul l'auteur du Projet peut le supprimer."},
                status=status.HTTP_403_FORBIDDEN
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
    permission_classes = [IsAuthor | IsContributor]
    lookup_field = 'issue_id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if self.action == 'list':
            # Vérifie si l'utilisateur est un contributeur du projet
            project = get_object_or_404(Project, project_id=project_id)
            if project.contributors.filter(pk=self.request.user.pk).exists():
                return Issue.objects.filter(project_id=project_id)
            else:
                raise PermissionDenied("Vous n'êtes pas autorisé à voir les issues de ce projet.")
        return Issue.objects.all()

    def perform_create(self, serializer):
        project_id = self.request.data.get('project_id')
        project = get_object_or_404(Project, project_id=project_id)
        serializer.save(author=self.request.user, project=project)

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')
        if action == 'update':
            instance = self.get_object()
            if request.user == instance.author:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "L'Issue a été modifiée avec succès."},
                        status=status.HTTP_200_OK
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise ValidationError("Seul l'auteur de l'issue peut la modifier.")

        elif action == 'destroy':
            instance = self.get_object()
            if request.user == instance.author:
                instance.delete()
                return Response(
                    {"message": "L'Issue a été supprimée avec succès."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise ValidationError("Seul l'auteur de l'issue peut la supprimer.")
        else:
            raise ValidationError("Action non valide.")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        if issue_id:
            return self.queryset.filter(issue_id=issue_id)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        issue_id = kwargs.get('issue_id')  # Utilisez kwargs pour récupérer issue_id

        # Vérifiez si l'issue existe
        issue = get_object_or_404(Issue, issue_id=issue_id)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, issue=issue)
            return Response(
                {"message": "Le commentaire a été créé avec succès."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            serializer = CommentSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Le commentaire a été modifié avec succès."},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError("Seul l'auteur du Comment peut le modifier.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            return Response(
                {"message": "Le Comment a été supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            raise ValidationError("Seul l'auteur du Comment peut le supprimer.")

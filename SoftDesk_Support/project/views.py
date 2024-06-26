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
from authentication.serializers import LoginSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthor, IsContributor, IsAuthenticated
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


class LoginView(viewsets.ViewSet):
    """Permet aux utilisateurs de se connecter."""
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            response['Location'] = '/api/projects/'
            response.status_code = status.HTTP_303_SEE_OTHER
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
            # Redirection après l'inscription
            response['Location'] = '/api/projects/'
            response.status_code = status.HTTP_303_SEE_OTHER
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    Permet de gérer les opérations suivantes sur le modèle Project :
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """

    permission_classes = [IsAuthor | IsContributor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    def get_queryset(self):
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')

        if action == 'update':
            instance = self.get_object()
            if request.user == instance.author:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
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
                return Response(
                    {"message": "Le projet a été supprimé avec succès."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise ValidationError("Seul l'auteur du Projet peut le supprimer.")

        else:
            raise ValidationError("Action non valide.")


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor | IsContributor]
    lookup_field = 'contributor_id'

    def get_project(self):
        project_id = self.kwargs['project_id']
        return get_object_or_404(Project, project_id=project_id)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project__project_id=project_id)

    def get_object(self):
        queryset = self.get_queryset()
        project_id = self.kwargs['project_id']
        contributor_id = self.kwargs['contributor_id']  # Adjust this according to your URL configuration
        obj = get_object_or_404(queryset, project__project_id=project_id, id=contributor_id)
        return obj

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

            contributor_id = request.data.get('contributor')
            if Contributor.objects.filter(project=project, contributor_id=contributor_id).exists():
                return Response({"detail": "L'utilisateur est déjà un contributeur de ce projet."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'destroy':
            instance = self.get_object()
            if request.user == project.author:
                self.perform_destroy(instance)
                return Response(
                    {"message": "Le Contributeur a été supprimé avec succès."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response({"detail": "Vous n'êtes pas autorisé à supprimer ce contributeur."},
                                status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": "Action non prise en charge."},
                        status=status.HTTP_400_BAD_REQUEST)


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
            project = get_object_or_404(Project, project_id=project_id)
            user = self.request.user
            if project.contributors.filter(pk=user.pk).exists() or project.author == user:
                return Issue.objects.filter(project_id=project_id)
            else:
                raise PermissionDenied("Vous n'êtes pas autorisé à voir les issues de ce projet.")
        return Issue.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')

        if action == 'create':
            project_id = request.data.get('project')
            project = get_object_or_404(Project, id=project_id)

            if not project.contributors.filter(id=request.user.id).exists():
                raise PermissionDenied("Vous n'êtes pas autorisé à créer des problèmes pour ce projet.")

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(
                    {"message": "Le problème a été créé avec succès."},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'update':
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
            return self.queryset.filter(issue__issue_id=issue_id)
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')

        if action == 'create':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(
                    {"message": "Le commentaire a été créé avec succès."},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'update':
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

        elif action == 'destroy':
            instance = self.get_object()
            if request.user == instance.author:
                instance.delete()
                return Response(
                    {"message": "Le Comment a été supprimé avec succès."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise ValidationError("Seul l'auteur du Comment peut le supprimer.")

        else:
            raise ValidationError("Action non valide.")

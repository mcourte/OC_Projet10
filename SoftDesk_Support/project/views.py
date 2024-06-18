from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Project, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from authentication.serializers import LoginSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthorOrContributor, IsAuthenticated
from authentication.permissions import AllowAnonymousAccess


class LoginView(viewsets.ViewSet):
    """
    Permet à toute personne accédant à l'application de se connecter ou de créer un compte.
    """
    permission_classes = [AllowAnonymousAccess]

    def create(self, request, *args, **kwargs):
        if 'action' in request.data and request.data['action'] == 'login':
            return self.login(request)
        elif 'action' in request.data and request.data['action'] == 'register':
            return self.register(request)
        else:
            return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeViewSet(viewsets.ModelViewSet):
    """Permet à toute personne identifié, de voir la liste de tous les Projets
    de voir la liste des projets où il est Contributeur, de créer un Projet."""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Project.objects.all()
        elif self.action == 'projects_as_contributor':
            return self.request.user.projects_as_contributor.all()

    def get(self, request, *args, **kwargs):
        if self.action == 'list':
            return self.list(request, *args, **kwargs)
        elif self.action == 'projects_as_contributor':
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProjectListViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Project.
    """

    permission_classes = [IsAuthorOrContributor]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProjectDetailViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Project.

    Create : Créer un projet.
    Read : Visualiser un projet.
    Update : Modifier un projet.
    Delete : Supprimer un projet.
    """

    permission_classes = [IsAuthorOrContributor | IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')

        if action == 'create':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(
                    {"message": "Le projet a été créé avec succès."},
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
    """
    Permet de gérer les opérations CRUD sur le modèle Contributor.

    Create : Créer un Contributor.
    Read : Visualiser un Contributor.
    Update : Modifier un Contributor.
    Delete : Supprimer un Contributor.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return self.project.contributors.all().order_by("created_time")

    def get_project(self):
        if not hasattr(self, '_project'):
            self._project = get_object_or_404(Project.objects.all().prefetch_related("contributors"),
                                              pk=self.kwargs["project_pk"])
        return self._project

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ContributorSerializer

        return super().get_serializer_class()

    def post(self, request, *args, **kwargs):
        action = request.data.get('action', 'create')

        if action == 'create':
            if request.user != self.project.author:
                raise ValidationError("Seul l'auteur du projet peut ajouter des contributeurs.")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.project.contributors.add(serializer.validated_data["user"])
                return Response(
                    {"message": "Le Contributeur a été ajouté avec succès."},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'destroy':
            if request.user == self.project.author:
                instance = self.get_object()
                self.project.contributors.remove(instance)
                return Response(
                    {"message": "Le Contributeur a été supprimé avec succès."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise ValidationError("Seul l'auteur du Projet peut supprimer des Contributeurs.")

        else:
            raise ValidationError("Action non valide.")


class IssueViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle Issue.

    Create : Créer une Issue.
    Read : Visualiser une Issue.
    Update : Modifier une Issue.
    Delete : Supprimer une Issue.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        if self.action == 'list':
            return Issue.objects.filter(project_id=self.kwargs.get('project_pk'), active=True)
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
    """
    Permet de gérer les opérations CRUD sur le modèle Comment.

    Create : Créer un Comment.
    Read : Visualiser un Comment.
    Update : Modifier un Comment.
    Delete : Supprimer un Comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        if self.action == 'list':
            return Comment.objects.filter(issue_id=self.kwargs.get('issue_pk'))
        return Comment.objects.all()

    @property
    def comment(self):
        if self._comment is None:
            self._comment = Comment.objects.filter(
                issue_id=self.kwargs["issue_pk"]
            )

        return self._comment

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

from rest_framework import permissions, viewsets, status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    RegisterSerializer
)
from .permissions import (
    IsAdmin,
    IsUser,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from authentication.serializers import LoginSerializer, RegisterSerializer


class RootView(APIView):
    """
    Redirige les utilisateurs non authentifiés vers la page de connexion,
    et les utilisateurs authentifiés vers la liste des projets.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('projects')


class LoginView(viewsets.ViewSet):
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
            # Redirection après la connexion
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


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CustomUser.
    """

    queryset = CustomUser.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        # Permet à l'admin de voir tous les utilisateurs, sinon chaque utilisateur ne voit que lui-même
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        elif self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        else:
            return CustomUser.objects.none()

    def get_permissions(self):
        """
        Retourne les permissions en fonction de l'action.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsUser | IsAdmin]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Retourne le serializer en fonction de l'action.
        """
        if self.action == 'list':
            return CustomUserListSerializer
        return CustomUserDetailSerializer

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.is_superuser and self.request.user != instance:
            return Response({"detail": "Vous n'êtes pas autorisé à modifier ce profil."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.is_superuser and self.request.user != instance:
            return Response({"detail": "Vous n'êtes pas autorisé à modifier ce profil."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_superuser or self.request.user == instance:
            return self.destroy(request, *args, **kwargs)
        return Response({"detail": "Vous n'êtes pas autorisé à supprimer ce profil."},
                        status=status.HTTP_403_FORBIDDEN)
  
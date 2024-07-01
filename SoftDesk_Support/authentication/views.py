from rest_framework import permissions, viewsets, status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserDetailSerializer
)
from .permissions import (
    IsAdmin,
    IsUser,
)


class RootView(APIView):
    """
    Redirige les utilisateurs non authentifiés vers la page de connexion,
    et les utilisateurs authentifiés vers la liste des projets.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('projects')


@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


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

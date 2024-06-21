from rest_framework import generics, permissions, viewsets, status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    RegisterSerializer,
    LoginSerializer
)
from .permissions import (
    IsAdmin,
    IsUser,
)


class LoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
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


class RootView(APIView):
    """
    Redirige les utilisateurs non authentifiés vers la page de connexion,
    et les utilisateurs authentifiés vers la liste des projets.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('projects')


class RegisterView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement d'un nouvel utilisateur.

    Cette vue permet de créer un nouveau compte utilisateur.
    """

    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny)
    serializer_class = RegisterSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CustomUser.

    - Create : Créer un CustomUser.
    - Read : Visualiser un CustomUser.
    - Update : Modifier un CustomUser.
    - Delete : Supprimer un CustomUser.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """
        Retourne les permissions en fonction de l'action.
        """
        if self.action == 'list':
            permission_classes = [IsAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsUser]
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

    def get(self, request, *args, **kwargs):
        """
        Gère les requêtes GET.
        """
        if self.action == 'list':
            return self.list(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour la création d'un utilisateur.
        """
        return super().create(request, *args, **kwargs)

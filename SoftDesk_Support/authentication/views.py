from rest_framework import generics, permissions, viewsets
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    RegisterSerializer
)
from .permissions import (
    IsAdmin,
    IsUser,
    AllowAnonymousAccess
)
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement d'un nouvel utilisateur.

    Cette vue permet de créer un nouveau compte utilisateur.
    """

    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour obtenir un token JWT.

    Cette vue permet à un utilisateur de s'authentifier et de recevoir un token JWT.
    """

    serializer_class = CustomUserListSerializer

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour l'obtention du token.

        Ajoute les informations de l'utilisateur au token retourné.
        """
        response = super().post(request, *args, **kwargs)
        response.data.update({'user': CustomUserListSerializer(self.user).data})
        return response


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

    def get_permissions(self):
        """
        Retourne les permissions en fonction de l'action.

        - list : Doit être administrateur.
        - create : Doit être authentifié.
        - retrieve, update, partial_update, destroy : Doit être l'utilisateur concerné.
        - Autres : Accès anonyme autorisé.
        """
        if self.action == 'list':
            permission_classes = [IsAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsUser]
        else:
            permission_classes = [AllowAnonymousAccess]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Retourne le serializer en fonction de l'action.

        - list : Utilise CustomUserListSerializer.
        - retrieve : Utilise CustomUserDetailSerializer.
        - create : Utilise CustomUserDetailSerializer.
        - update : Utilise CustomUserDetailSerializer.
        - Autres : Utilise CustomUserDetailSerializer.
        """
        if self.action == 'list':
            return CustomUserListSerializer
        elif self.action == 'retrieve':
            return CustomUserDetailSerializer
        elif self.action == 'create':
            return CustomUserDetailSerializer
        elif self.action == 'update':
            return CustomUserDetailSerializer
        return CustomUserDetailSerializer

    def get(self, request, *args, **kwargs):
        """
        Gère les requêtes GET.

        - list : Retourne la liste des utilisateurs.
        - retrieve : Retourne les détails d'un utilisateur spécifique.
        """
        if self.action == 'list':
            return self.list(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour la création d'un utilisateur.

        Utilise la méthode create de ModelViewSet.
        """
        return super().create(request, *args, **kwargs)

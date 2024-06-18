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
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserListSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data.update({'user': CustomUserListSerializer(self.user).data})
        return response


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CustomUser.

    Create : Créer un CustomUser.
    Read : Visualiser un CustomUser.
    Update : Modifier un CustomUser.
    Delete : Supprimer un CustomUser.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer

    def get_permissions(self):
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
        if self.action == 'list':
            return self.list(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

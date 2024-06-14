from rest_framework import viewsets
from rest_framework import permissions
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserUpdateSerializer,
    CustomUserCreateSerializer,
    CustomUserDetailSerializer
)
from .permissions import (
    IsAdmin,
    IsUser,
    AllowAnonymousAccess
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['next'] = '/projects/'
        return response


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CustomUser.

    Create : Créer un CustomUser.
    Read : Visualiser un CustomUser.
    Update : Modifier un CustomUser.
    Delete : Supprimer un CustomUser.
    """

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

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
            return CustomUserCreateSerializer
        elif self.action == 'update':
            return CustomUserUpdateSerializer
        return CustomUserDetailSerializer

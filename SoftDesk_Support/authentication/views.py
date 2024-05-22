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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

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

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAdmin]
        elif self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsUser]
        else:
            permission_classes = [AllowAnonymousAccess]

        return [permission() for permission in permission_classes]

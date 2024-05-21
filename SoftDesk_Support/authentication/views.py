from rest_framework import viewsets
from .models import CustomUser
from .serializers import (
    CustomUserListSerializer,
    CustomUserUpdateSerializer,
    CustomUserCreateSerializer,
    CustomUserDetailSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminAuthenticated,
    AllowAnonymousAccess
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    serializer_mapping = {
        "list": CustomUserListSerializer,
        "retrieve": CustomUserDetailSerializer,
        "create": CustomUserCreateSerializer,
        "update": CustomUserUpdateSerializer,
        "partial_update": CustomUserUpdateSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la liste des permissions nécessaires pour chaque action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_permissions(self):

        if self.action == "retrieve":
            permission_classes = [IsAdmin]
        elif self.action in [
            "list",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsAdminAuthenticated]
        elif self.action == "create":
            permission_classes = [AllowAnonymousAccess]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CustomUser.objects.all().order_by("id")

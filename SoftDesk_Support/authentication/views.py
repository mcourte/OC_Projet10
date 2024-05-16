from rest_framework import viewsets
# from .models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les opérations CRUD sur le modèle CustomUser.

    Create : Créer un User.
    Read : Visualiser un User.
    Update : Modifier un User.
    Delete : Supprimer un User.
    """

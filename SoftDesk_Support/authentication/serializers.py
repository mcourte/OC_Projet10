from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class CustomUserCreateSerializer(ModelSerializer):
    """
    Sérialiseur pour créer une nouvelle instance CustomUser.

    Ce sérialiseur est utilisé pour créer une nouvelle instance CustomUser.
    Il inclut les champs pour le nom d'utilisateur, le mot de passe, la date de naissance,
    peut_être_contacté, peut_partager_des_données et heure_de_création.
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        )


class CustomUserListSerializer(ModelSerializer):
    """
    Sérialiseur pour répertorier les instances CustomUser.

    Ce sérialiseur est utilisé pour répertorier les instances CustomUser.
    Il inclut les champs pour l'identifiant, le nom d'utilisateur et le mot de passe.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
        ]


class CustomUserDetailSerializer(ModelSerializer):
    """
    Sérialiseur pour récupérer des informations détaillées sur une instance CustomUser.

    Ce sérialiseur est utilisé pour récupérer des informations détaillées sur une instance CustomUser.
    Il inclut les champs pour l'identifiant, le nom d'utilisateur, le mot de passe, la date de naissance,
    peut_être_contacté, peut_partager_des_données et heure_de_création.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        ]


class CustomUserUpdateSerializer(ModelSerializer):
    """
    Sérialiseur pour mettre à jour une instance CustomUser.

    Ce sérialiseur est utilisé pour mettre à jour une instance CustomUser.
    Il inclut les champs pour le nom d'utilisateur, le mot de passe, la date de naissance,
    peut_être_contacté et peut_partager_des_données.
    """

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        ]


class CustomUserAuthorContributorSerializer(ModelSerializer):
    """
    Sérialiseur pour répertorier les instances CustomUser en tant qu'auteurs ou contributeurs.

    Ce sérialiseur est utilisé pour répertorier les instances CustomUser en tant qu'auteurs ou contributeurs.
    Il inclut les champs pour l'identifiant et le nom d'utilisateur.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
        ]

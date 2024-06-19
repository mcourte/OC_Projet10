from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """
    Sérialiseur pour la connexion des utilisateurs.

    Ce sérialiseur valide les informations d'identification de l'utilisateur
    et authentifie l'utilisateur en utilisant le nom d'utilisateur et le mot de passe.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Valide les données de connexion fournies par l'utilisateur.

        Args:
            data (dict): Les données de connexion comprenant le nom d'utilisateur et le mot de passe.

        Raises:
            serializers.ValidationError: Si le nom d'utilisateur ou le mot de passe est incorrect,
                                          ou s'ils ne sont pas fournis.

        Returns:
            dict: Les données validées, incluant l'utilisateur authentifié.
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')

        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'enregistrement des utilisateurs.

    Ce sérialiseur est utilisé pour créer un nouvel utilisateur avec les champs spécifiés.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.

        Args:
            validated_data (dict): Les données validées pour créer un nouvel utilisateur.

        Returns:
            CustomUser: L'instance nouvellement créée de l'utilisateur.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        return user


class CustomUserListSerializer(serializers.ModelSerializer):
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


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour récupérer des informations détaillées sur une instance CustomUser.

    Ce sérialiseur est utilisé pour récupérer des informations détaillées sur une instance CustomUser.
    Il inclut les champs pour l'identifiant, le nom d'utilisateur, le mot de passe, la date de naissance,
    le consentement pour être contacté, le consentement pour partager des données, et la date de création.
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


class CustomUserAuthorContributorSerializer(serializers.ModelSerializer):
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

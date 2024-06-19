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

        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Nom d'utilisateur ou mot de passe invalide")
        else:
            raise serializers.ValidationError("Les champs 'Nom d'utilisateur' et ' mot de passe' doivent être remplis")

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

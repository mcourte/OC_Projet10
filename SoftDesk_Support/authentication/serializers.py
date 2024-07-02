from .models import CustomUser
from rest_framework import serializers


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour répertorier les instances CustomUser.

    Ce sérialiseur est utilisé pour répertorier les instances CustomUser.
    Il inclut les champs pour l'identifiant et le nom d'utilisateur.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
        ]


class CustomUserDetailSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'enregistrement des utilisateurs.
    Ce sérialiseur est utilisé pour créer un nouvel utilisateur avec les champs spécifiés.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']

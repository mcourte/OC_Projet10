from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
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
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
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

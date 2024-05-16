from rest_framework import serializers
from authentication.models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
            "id_user"
        )

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_age(value):
    """
    Valide que la date de naissance correspond à un âge supérieur à 15 ans.
    """
    today = timezone.now().date()
    age = today - value
    if age < timedelta(days=15*365):
        raise ValidationError('Vous devez avoir plus de 15 ans pour vous inscrire.')


class CustomUser(AbstractUser):
    """
    Modèle d'utilisateur personnalisé.
    """

    username = models.CharField(max_length=20, unique=True)

    password = models.CharField(max_length=12, unique=False)

    date_of_birth = models.DateField(
        verbose_name="date of birth",
        default=timezone.now,
        validators=[validate_age]
    )

    can_be_contacted = models.BooleanField(
        default=False,
        verbose_name="contact consent"
    )

    can_data_be_shared = models.BooleanField(
        default=False,
        verbose_name="share consent"
    )

    id_user = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    created_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="date de création"
    )

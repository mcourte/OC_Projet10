from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_age(value):
    today = timezone.now().date()
    age = today - value
    if age < timedelta(days=15*365):
        raise ValidationError('You must be over 15 years old.')


class CustomUser(AbstractUser):
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

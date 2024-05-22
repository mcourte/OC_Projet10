from django.contrib import admin
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_of_birth",
        "can_be_contacted",
        "can_data_be_shared",
        "created_time",
    )


admin.site.register(CustomUser, CustomUserAdmin)

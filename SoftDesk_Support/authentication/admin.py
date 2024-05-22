from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin (admin.ModelAdmin):
    list_display = ('username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared', 'id_user')


admin.site.register(CustomUser, CustomUserAdmin)

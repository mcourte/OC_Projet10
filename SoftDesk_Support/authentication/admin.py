from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire personnalisé pour la création d'un utilisateur.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')


class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire personnalisé pour la modification d'un utilisateur.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')


class CustomUserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle CustomUser.
    """

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


# Enregistrement du modèle CustomUser avec l'interface d'administration personnalisée.
admin.site.register(CustomUser, CustomUserAdmin)

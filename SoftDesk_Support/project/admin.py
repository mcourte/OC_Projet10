from django.contrib import admin
from .models import Project, Issue, Comment, Contributor


class ContributorInline(admin.TabularInline):
    """
    Classe pour afficher les contributeurs en ligne dans l'interface d'administration.
    """
    model = Contributor
    extra = 1  # Nombre de formulaires supplémentaires à afficher


class ProjectAdmin(admin.ModelAdmin):
    """
    Classe pour personnaliser l'affichage du modèle Project dans l'interface d'administration.
    """
    list_display = (
        'name',
        'project_type',
        'description',
        'created_time',
        'updated_time',
        'contributor_owner',
    )
    search_fields = ('name', 'project_type', 'description')
    fields = (
        'name',
        'project_type',
        'description',
        'contributor_owner',
    )
    readonly_fields = ('created_time', 'updated_time')
    list_filter = ('project_type', 'created_time', 'updated_time', 'contributor_owner')
    inlines = [ContributorInline]  # Ajout de l'inline admin ici


class IssueAdmin(admin.ModelAdmin):
    """
    Classe pour personnaliser l'affichage du modèle Issue dans l'interface d'administration.
    """

    list_display = ('title', 'get_project_name',)

    def get_project_name(self, obj):
        """
        Obtient le nom du projet associé à cette issue.
        """
        return obj.project.name

    get_project_name.short_description = 'Project'


class CommentAdmin(admin.ModelAdmin):
    """
    Classe pour personnaliser l'affichage du modèle Comment dans l'interface d'administration.
    """

    list_display = ('name', 'get_project_name', 'issue',)

    @admin.display(description='Project')
    def get_project_name(self, obj):
        """
        Obtient le nom du projet associé à ce commentaire.
        """
        return obj.issue.project.name


# Enregistrement des modèles et de leurs configurations dans l'interface d'administration
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from .models import Project, Issue, Comment, Contributor


class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1  # Nombre de formulaires supplémentaires à afficher


class ProjectAdmin(admin.ModelAdmin):
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
    list_display = ('title', 'get_project_name',)

    def get_project_name(self, obj):
        return obj.project.name

    get_project_name.short_description = 'Project'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_project_name', 'issue',)

    @admin.display(description='Project')
    def get_project_name(self, obj):
        return obj.issue.project.name


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from .models import Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_project_name',)

    def get_project_name(self, obj):
        return obj.project.name

    get_project_name.short_description = 'Project'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'issue',)

    @admin.display(description='Project')
    def project(self, obj):
        return obj.issue.project


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

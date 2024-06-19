from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, Contributor
from rest_framework import serializers
from authentication.serializers import CustomUserAuthorContributorSerializer


class ProjectListSerializer(ModelSerializer):
    """Serializer pour lister les PROJECT."""

    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "project_id",
            "name",
            "author",
            "contributors",
        ]


class ProjectSerializer(ModelSerializer):
    """Serializer pour afficher des informations détaillées sur un PROJECT."""

    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "project_id",
            "created_time",
            "name",
            "description",
            "project_type",
            "author",
            "contributors",
        ]


class IssueSerializer(ModelSerializer):
    """Serializer pour créer une ISSUE."""
    project_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Issue
        fields = [
            'issue_id',
            'title',
            'author',
            'description',
            'priority',
            'tag',
            'status',
            'assigned_to',
            'created_time',
            'project_id',
        ]


class CommentSerializer(ModelSerializer):
    """Serializer pour créer un COMMENT."""

    class Meta:
        model = Comment
        fields = [
            'comment_id',
            'created_time',
            'author',
            'name',
            'description',
            'issue_id',
        ]


class ContributorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='contributor.username')
    created_time = serializers.ReadOnlyField(source='contributor.created_time')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributor
        fields = [
            "id",
            "username",
            "created_time",
            "project"
        ]

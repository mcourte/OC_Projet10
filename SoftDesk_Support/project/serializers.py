from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, CustomUser
from rest_framework import serializers
from authentication.serializers import CustomUserAuthorContributorSerializer


class ProjectListSerializer(ModelSerializer):
    """Serializer pour lister les PROJECT."""

    contributor_owner = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "project_id",
            "name",
            "contributor_owner",
            "contributors",
        ]


class ProjectSerializer(ModelSerializer):
    """Serializer pour afficher des informations détaillées sur un PROJECT."""

    contributor_owner = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "project_id",
            "created_time",
            "name",
            "description",
            "project_type",
            "contributor_owner",
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
            'active'
        ]


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer pour afficher des informations détaillées sur un CONTRIBUTOR."""

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        ]

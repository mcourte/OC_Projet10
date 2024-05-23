from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, CustomUser
from rest_framework import serializers
from authentication.serializers import CustomUserAuthorContributorSerializer


class ProjectListSerializer(ModelSerializer):
    """Serializer pour lister les PROJECT."""

    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
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
            "id",
            "created_time",
            "name",
            "description",
            "project_type",
            "author",
            "contributors",
        ]


class IssueSerializer(ModelSerializer):
    """Serializer pour créer une ISSUE."""

    class Meta:
        model = Issue
        fields = [
            "id",
            "assigned_to",
            "title",
            "description",
            "tag",
            "status",
            "priority",
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

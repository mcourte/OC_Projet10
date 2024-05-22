from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, CustomUser
from rest_framework import serializers
from authentication.serializers import CustomUserAuthorContributorSerializer


class ProjectCreateSerializer(ModelSerializer):
    """Serializer pour créer un PROJECT."""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "project_type",
        ]


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


class ProjectDetailSerializer(ModelSerializer):
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


class ProjectUpdateSerializer(ModelSerializer):
    """Serializer pour mettre à jour des instances de PROJECT."""

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "project_type",
        ]


class ProjectSerializer(ModelSerializer):
    """Serializer pour le projet."""

    class Meta:
        model = Project
        fields = [
            'name',
            'project_type',
            'description',
            'created_time',
            'updated_time',
            'contributor_owner',
            'contributors'
        ]


class IssueCreateSerializer(ModelSerializer):
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
            "active"
        ]


class IssueListSerializer(ModelSerializer):
    """Serializer pour lister les ISSUE."""

    project = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'author',
            'title',
            'description',
            'priority',
            'tag',
            'status',
            'assigned_to',
            'created_time',
        ]


class IssueDetailSerializer(ModelSerializer):
    """Serializer pour afficher des informations détaillées sur une ISSUE."""
    project = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'author',
            'project_id',
            'issue_id',
            'title',
            'description',
            'priority',
            'tag',
            'status',
            'assigned_to',
            'created_time',
            'active'
        ]

    def get_articles(self, instance):
        queryset = instance.project.filter(active=True)
        serializer = ProjectSerializer(queryset, many=True)
        return serializer.data


class CommentCreateSerializer(ModelSerializer):
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


class CommentListSerializer(ModelSerializer):
    """Serializer pour lister les COMMENT."""
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'author',
            'name',
            'description',
        ]


class CommentDetailSerializer(ModelSerializer):
    """Serializer pour afficher des informations détaillées sur un COMMENT."""
    issue = serializers.SerializerMethodField()

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

    def get_products(self, instance):
        queryset = instance.issue.filter(active=True)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer les CONTRIBUTOR"""

    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class ContributorDetailSerializer(serializers.ModelSerializer):
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

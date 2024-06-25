from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from authentication.models import CustomUser


class CustomUserAuthorContributorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ProjectListSerializer(serializers.ModelSerializer):
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


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_type']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer pour afficher des informations détaillées sur un PROJECT."""
    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)
    issues_count = serializers.SerializerMethodField()
    issue_titles = serializers.SerializerMethodField()

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
            'issues_count',
            'issue_titles'
        ]

    def get_issues_count(self, obj):
        return Issue.objects.filter(project=obj).count()

    def get_issue_titles(self, obj):
        issues = Issue.objects.filter(project=obj).values_list('title', flat=True)
        return list(issues)


class IssueSerializer(serializers.ModelSerializer):
    """Serializer pour créer une ISSUE."""
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', read_only=False)
    comment_count = serializers.SerializerMethodField()
    comment_titles = serializers.SerializerMethodField()
    author = CustomUserAuthorContributorSerializer()

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
            'comment_count',
            'comment_titles'
        ]

    def get_comment_count(self, obj):
        return Comment.objects.filter(issue=obj).count()

    def get_comment_titles(self, obj):
        comments = Comment.objects.filter(issue=obj).values_list('name', flat=True)
        return list(comments)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour créer un COMMENT."""
    issue_id = serializers.SerializerMethodField()

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

    def get_issue_id(self, obj):
        return obj.issue.issue_id


class ContributorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='contributor.username')

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ['project']

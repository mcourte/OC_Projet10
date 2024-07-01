from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from authentication.models import CustomUser


class CustomUserAuthorContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CustomUser, utilisé pour afficher les informations de l'auteur ou du contributeur.
    """
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer pour lister les projets.
    """
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
    """
    Serializer pour créer ou modifier un projet.
    """
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_type']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher des informations détaillées sur un projet.
    """
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
        """
        Retourne le nombre d'issues pour un projet donné.
        """
        return Issue.objects.filter(project=obj).count()

    def get_issue_titles(self, obj):
        """
        Retourne une liste de dictionnaires contenant l'ID et le titre de chaque issue associée au projet.
        """
        issues = Issue.objects.filter(project=obj).values('issue_id', 'title')
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
    """Serializer pour créer un commentaire."""

    issue_id = serializers.PrimaryKeyRelatedField(source='issue', read_only=True)

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
    """
    Serializer pour ajouter un contributeur.
    """
    username = serializers.ReadOnlyField(source='contributor.username')

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ['project']

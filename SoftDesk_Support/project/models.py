from django.db import models
import uuid
from django.conf import settings
from authentication.models import CustomUser


class Project(models.Model):
    PROJECT_TYPES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    project_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="project ID",
        help_text="Unique ID of the project"
    )
    name = models.CharField(max_length=255, help_text='Name of project')
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPES, help_text='Type of project')
    description = models.TextField(blank=False, help_text='Description of the project')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='updated date')
    contributor_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        null=True,
        blank=True
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='contributions',
        help_text='Project contributors'
    )

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """Model representing a contributor."""

    contributor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributor_relationship",
        help_text="Project to which the contributor contributes",
    )

    def __str__(self):
        return f"{self.contributor.username} - {self.project.name}"


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]

    STATUS_CHOICES = [
        ("TO_DO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_authors",
        verbose_name="issue author",
        help_text="Issue author"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
        verbose_name="related project",
        help_text="Project to which the issue belongs"
    )

    issue_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="issue ID",
        help_text="Unique ID of the issue"
    )

    title = models.CharField(
        max_length=255,
        help_text="Title of the issue"
    )

    description = models.TextField(
        help_text="Description of the issue"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
        help_text="Issue priority"
    )

    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        default="BUG",
        help_text="Tag of the issue"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TO_DO",
        help_text="Status of the issue"
    )

    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
        help_text="User assigned to the issue"
    )

    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created time"
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Comment(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created time"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_authors"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="comment name",
        help_text="Comment name"
    )

    description = models.TextField(
        verbose_name="comment body",
        help_text="Comment body"
    )

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comments",
        verbose_name=("related issue"),
        help_text="Issue associated with comment",
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} | {self.issue}"

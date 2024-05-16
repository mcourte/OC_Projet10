from django.db import models
import uuid
from django.conf import settings


class Project(models.Model):
    PROJECT_TYPES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

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

    project_id = models.UUIDField(
        verbose_name="project ID",
        help_text="ID of the project to which the issue belongs"
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

    issue_id = models.UUIDField(
        verbose_name="issue ID",
        help_text="ID of the issue to which the comment belongs"
    )

    def __str__(self):
        return self.name

from django.db import models
import uuid
from django.conf import settings
from authentication.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


def get_admin_user():
    """
    Fonction pour récupérer l'utilisateur administrateur.
    """
    User = get_user_model()
    try:
        return User.objects.filter(is_superuser=True).first()
    except ObjectDoesNotExist:
        return None


class Project(models.Model):
    """
    Modèle représentant un projet.
    """

    PROJECT_TYPES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    project_id = models.CharField(
        max_length=50,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name="project ID",
        help_text="Identifiant unique du projet"
    )

    name = models.CharField(max_length=255, help_text='Nom du projet')

    project_type = models.CharField(max_length=10, choices=PROJECT_TYPES, help_text='Type de projet')

    description = models.TextField(blank=False, help_text='Description du projet')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='date de création')

    updated_time = models.DateTimeField(auto_now=True, verbose_name='date de mise à jour')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_admin_user),
        related_name='owned_projects',
        null=True,
        blank=True,
        verbose_name="propriétaire du projet"
    )

    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='contributions',
        help_text='Contributeurs du projet'
    )

    def generate_project_id(self):
        """
        Génère un identifiant unique pour le projet basé sur ses initiales.
        """
        initials = ''.join([word[0].upper() for word in self.name.split()])
        base_id = f"project_{initials}"
        similar_ids = Project.objects.filter(project_id__startswith=base_id).values_list('project_id', flat=True)

        if not similar_ids:
            return base_id

        suffix = 1
        new_id = f"{base_id}_{suffix}"
        while new_id in similar_ids:
            suffix += 1
            new_id = f"{base_id}_{suffix}"

        return new_id

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save() pour générer un project_id s'il n'est pas défini.
        """
        if not self.project_id:
            self.project_id = self.generate_project_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """
    Modèle représentant un contributeur d'un projet.
    """

    contributor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributor_relationship",
        help_text="Projet auquel le contributeur contribue",
    )

    def __str__(self):
        return f"{self.contributor.username} - {self.project.name}"


class Issue(models.Model):
    """
    Modèle représentant une issue d'un projet.
    """

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
        ("TO_DO", "to do"),
        ("IN_PROGRESS", "in_progress"),
        ("FINISHED", "finished"),
    ]

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_admin_user),
        related_name="issue_authors",
        verbose_name="auteur de l'issue",
        help_text="Auteur de l'issue"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
        verbose_name="projet associé",
        help_text="Projet auquel l'issue appartient",
        null=False,
        blank=False
    )

    issue_id = models.PositiveIntegerField(
        editable=False,
        unique=True,
        verbose_name="ID de l'issue",
        help_text="Identifiant unique de l'issue"
    )

    title = models.CharField(
        max_length=255,
        help_text="Titre de l'issue"
    )

    description = models.TextField(
        help_text="Description de l'issue"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
        help_text="Priorité de l'issue"
    )

    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        default="BUG",
        help_text="Catégorie de l'issue"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TO_DO",
        help_text="Statut de l'issue"
    )

    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_admin_user),
        null=True,
        blank=True,
        related_name="assigned_issues",
        verbose_name="utilisateur assigné",
        help_text="Utilisateur assigné à l'issue"
    )

    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date de création"
    )

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save() pour générer un issue_id s'il n'est pas défini.
        """
        if not self.issue_id:
            last_issue = Issue.objects.filter(project=self.project).order_by('issue_id').last()
            if last_issue:
                self.issue_id = last_issue.issue_id + 1
            else:
                self.issue_id = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Comment(models.Model):
    """
    Modèle représentant un commentaire sur une issue.
    """
    comment_id = models.UUIDField(
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
        on_delete=models.SET(get_admin_user),
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

    def __str__(self):
        return f"{self.name} | {self.issue}"

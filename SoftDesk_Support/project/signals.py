from django.db.models.signals import pre_delete
from django.dispatch import receiver
from authentication.models import CustomUser
from .models import Project, Issue, Comment


@receiver(pre_delete, sender=CustomUser)
def reassign_user_projects_issues_comments(sender, instance, **kwargs):
    admin_user = CustomUser.objects.filter(is_superuser=True).first()  # Récupérer un utilisateur administrateur
    if not admin_user:
        raise ValueError("Aucun utilisateur administrateur trouvé pour réattribuer les projets.")

    # Réaffecter les projets
    projects = Project.objects.filter(contributor_owner=instance)
    for project in projects:
        project.contributor_owner = admin_user
        project.save()

    # Réaffecter les issues
    issues = Issue.objects.filter(author=instance)
    for issue in issues:
        issue.author = issue.project.contributor_owner
        issue.save()

    # Réaffecter les commentaires
    comments = Comment.objects.filter(author=instance)
    for comment in comments:
        comment.author = comment.issue.project.contributor_owner
        comment.save()

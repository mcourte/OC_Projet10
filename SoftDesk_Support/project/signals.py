from django.db.models.signals import pre_delete
from django.dispatch import receiver
from authentication.models import CustomUser
from .models import Project, Issue, Comment


@receiver(pre_delete, sender=CustomUser)
def reassign_user_projects_issues_comments(sender, instance, **kwargs):
    """
    Fonction de signal pour réaffecter les projets, issues et commentaires d'un utilisateur avant sa suppression.

    Lorsqu'un utilisateur CustomUser est supprimé, cette fonction est déclenchée pour réaffecter ses projets,
    issues et commentaires à un utilisateur administrateur existant.

    Args:
        sender (CustomUser): Le modèle CustomUser qui envoie le signal.
        instance (CustomUser): L'instance de l'utilisateur CustomUser qui est en train d'être supprimée.
        **kwargs: Arguments supplémentaires liés au signal.

    Raises:
        ValueError: Si aucun utilisateur administrateur n'est trouvé pour réattribuer les projets.

    Notes:
        Cette fonction suppose l'existence d'au moins un utilisateur administrateur (is_superuser=True)
        dans le système.
        Les projets seront réattribués à l'utilisateur administrateur.
        Les issues seront réattribuées à l'utilisateur propriétaire du projet associé.
        Les commentaires seront réattribués à l'utilisateur propriétaire du projet de l'issue associée.
    """
    admin_user = CustomUser.objects.filter(is_superuser=True).first()  # Récupérer un utilisateur administrateur
    if not admin_user:
        raise ValueError("Aucun utilisateur administrateur trouvé pour réattribuer les projets.")

    # Réaffecter les projets
    projects = Project.objects.filter(author=instance)
    for project in projects:
        project.author = admin_user
        project.save()

    # Réaffecter les issues
    issues = Issue.objects.filter(author=instance)
    for issue in issues:
        issue.author = issue.project.author
        issue.save()

    # Réaffecter les commentaires
    comments = Comment.objects.filter(author=instance)
    for comment in comments:
        comment.author = comment.issue.project.author
        comment.save()

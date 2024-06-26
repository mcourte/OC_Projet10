# Generated by Django 5.0.6 on 2024-07-01 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_alter_contributor_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_authors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(help_text='Issue associated with comment', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='project.issue', verbose_name='related issue'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issue_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name="ID de l'issue"),
        ),
    ]

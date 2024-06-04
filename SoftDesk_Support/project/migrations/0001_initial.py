# Generated by Django 5.0.6 on 2024-06-03 15:43

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID of the issue', unique=True, verbose_name='issue ID')),
                ('title', models.CharField(help_text='Title of the issue', max_length=255)),
                ('description', models.TextField(help_text='Description of the issue')),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM', help_text='Issue priority', max_length=20)),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')], default='BUG', help_text='Tag of the issue', max_length=20)),
                ('status', models.CharField(choices=[('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')], default='TO_DO', help_text='Status of the issue', max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('assigned_to', models.ForeignKey(blank=True, help_text='User assigned to the issue', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_issues', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(help_text='Issue author', on_delete=django.db.models.deletion.CASCADE, related_name='issue_authors', to=settings.AUTH_USER_MODEL, verbose_name='issue author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('name', models.CharField(help_text='Comment name', max_length=100, verbose_name='comment name')),
                ('description', models.TextField(help_text='Comment body', verbose_name='comment body')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_authors', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(blank=True, help_text='Issue associated with comment', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='project.issue', verbose_name='related issue')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID of the project', primary_key=True, serialize=False, unique=True, verbose_name='project ID')),
                ('name', models.CharField(help_text='Name of project', max_length=255)),
                ('project_type', models.CharField(choices=[('Backend', 'Backend'), ('Frontend', 'Frontend'), ('iOS', 'iOS'), ('Android', 'Android')], help_text='Type of project', max_length=10)),
                ('description', models.TextField(help_text='Description of the project')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('contributor_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_projects', to=settings.AUTH_USER_MODEL)),
                ('contributors', models.ManyToManyField(help_text='Project contributors', related_name='contributions', through='project.Contributor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(help_text='Project to which the issue belongs', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='project.project', verbose_name='related project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(help_text='Project to which the contributor contributes', on_delete=django.db.models.deletion.CASCADE, related_name='contributor_relationship', to='project.project'),
        ),
    ]

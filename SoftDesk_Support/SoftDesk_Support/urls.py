"""
URL configuration for SoftDesk_Support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import CustomUserViewSet, CustomTokenObtainPairView
from project.views import (
    ProjectDetailViewSet,
    ProjectListViewSet,
    IssueViewSet,
    CommentViewSet,
    ContributorViewSet,
)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('authentication.urls')),
    path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user'),
    path('projects/', ProjectListViewSet.as_view({'get': 'list'}), name='projects'),
    path('projects/<int:project_id>/', ProjectDetailViewSet.as_view({'get': 'retrieve'}), name='project'),
    path('projects/<int:project_id>/contributors/', ContributorViewSet.as_view({'get': 'list'}), name='contributors'),
    path('projects/<int:project_id>/issues/', IssueViewSet.as_view({'get': 'list'}), name='issues'),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssueViewSet.as_view({'get': 'retrieve'}), name='issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentViewSet.as_view({'get': 'list'}),
         name='comments'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/',
         CommentViewSet.as_view({'get': 'retrieve'}), name='comment'),
]

# Redirect root to the API login
urlpatterns += [
    path('', lambda request: HttpResponseRedirect('/api-auth/login/'), name='root_redirect'),
]

# Debug URL for browsable API login
if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

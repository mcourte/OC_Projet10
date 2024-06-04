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

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from rest_framework_nested import routers
from authentication.views import CustomUserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from project.views import ProjectDetailViewSet, IssueViewSet, CommentViewSet, ContributorViewSet
from django.conf import settings

# Main router
router = routers.DefaultRouter()
router.register('projects', ProjectDetailViewSet, basename='project')
router.register('user', CustomUserViewSet, basename='user')

# Nested routers for project-related paths
project_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
project_router.register('contributors', ContributorViewSet, basename='project-contributors')
project_router.register('issues', IssueViewSet, basename='project-issues')

# Nested router for issue-related paths within projects
issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issue')
issue_router.register('comments', CommentViewSet, basename='issue-comments')

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
    path('api/', include(issue_router.urls)),
]


# Rediriger la racine vers l'API
urlpatterns += [
    path('', lambda request: HttpResponseRedirect('api/')),
]

if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

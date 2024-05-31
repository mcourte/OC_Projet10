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
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import CustomUserViewSet
from project.views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet


auth_api_urls = []
if settings.DEBUG:
    auth_api_urls.append(path(r"verify/", include("rest_framework.urls")))
# Routeur principal : Gère les routes pour les projets et les utilisateurs.
router = routers.DefaultRouter()
router.register('api/projects', ProjectViewSet, basename='project')
router.register('api/user', CustomUserViewSet, basename='user')

# Routeur imbriqué pour les projets : Gère les contributeurs et les issues pour un projet spécifique.
project_router = nested_routers.NestedSimpleRouter(router, 'api/projects', lookup='project')
project_router.register('contributors', ContributorViewSet, basename='project-contributors')
project_router.register('issues', IssueViewSet, basename='project-issues')

# Routeur imbriqué pour les issues :  Gère les commentaires pour une issue spécifique.
issue_router = nested_routers.NestedSimpleRouter(project_router, 'issues', lookup='issue')
issue_router.register('comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
    path('api/', include(issue_router.urls)),
]

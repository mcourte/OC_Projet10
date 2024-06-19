from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from authentication.views import (
    CustomTokenObtainPairView, CustomUserViewSet
)
from project.views import (
    LoginView, HomeViewSet, ProjectDetailViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
)


class RootView(APIView):
    """
    Redirige les utilisateurs non authentifiés vers la page de connexion,
    et les utilisateurs authentifiés vers la liste des projets.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('projects')


urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('admin/', admin.site.urls, name="admin"),

    # Token URLs
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registration and Login URLs
    path('api/login/', LoginView.as_view({'post': 'create'}), name='login'),

    # Authentication URLs
    path('api-auth/', include('rest_framework.urls')),

    # User URLs
    path('api/users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('api/users/<int:pk>/',
         CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                    'delete': 'destroy'}), name='user'),

    # Project URLs
    path('api/projects/', HomeViewSet.as_view({'get': 'list', 'post': 'create'}), name='projects'),
    path('api/projects/<int:pk>/',
         ProjectDetailViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                       'delete': 'destroy'}), name='project'),

    # Contributor URLs
    path('api/projects/<int:project_pk>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}), name='contributors'),
    path('api/projects/<int:project_pk>/contributors/<int:pk>/',
         ContributorViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='contributor'),

    # Issue URLs
    path('api/projects/<int:project_pk>/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='issues'),
    path('api/projects/<int:project_pk>/issues/<int:pk>/',
         IssueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                               'delete': 'destroy'}), name='issue'),

    # Comment URLs
    path('api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                 'delete': 'destroy'}), name='comment'),
]

if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

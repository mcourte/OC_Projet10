from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import CustomUserViewSet
from project.views import (
    LoginView,
    ProjectDetailViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
    HomeViewSet
)

router = DefaultRouter()
router.register(r'api/login', LoginView, basename='login')

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api/token/', LoginView.as_view({'post': 'login'}), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/', CustomUserViewSet.as_view({'get': 'list'}), name='users'),
    path('api/users/<int:user_id>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user'),

    path('api/projects/', HomeViewSet.as_view({'get': 'list', 'post': 'post'}), name='projects'),
    path('api/projects/<int:project_id>/', ProjectDetailViewSet.as_view({'get': 'retrieve', 'post': 'post'}),
         name='project'),

    path('api/projects/<int:project_id>/contributors/', ContributorViewSet.as_view({'get': 'list', 'post': 'post'}),
         name='contributors'),
    path('api/projects/<int:project_id>/contributors/<int:pk>/',
         ContributorViewSet.as_view({'get': 'retrieve', 'post': 'post', 'put': 'put',
                                     'patch': 'update', 'delete': 'destroy'}), name='contributor_detail'),

    path('api/projects/<int:project_id>/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'post'}),
         name='issues'),
    path('api/projects/<int:project_id>/issues/<int:pk>/',
         IssueViewSet.as_view({'get': 'retrieve', 'post': 'post', 'put': 'put',
                               'patch': 'update', 'delete': 'destroy'}), name='issue_detail'),

    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'post'}), name='comments'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'post': 'post', 'put': 'put',
                                 'patch': 'update', 'delete': 'destroy'}), name='comment_detail'),

    path('api/register/', LoginView.as_view({'post': 'register'}), name='register'),
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login for development
    path('', include(router.urls)),  # Includes the router URLs for login
]

if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

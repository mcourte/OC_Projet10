from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import (
     RootView,
     CustomUserViewSet,
     RegisterView
)
from project.views import (
     ProjectListViewSet,
     ProjectDetailViewSet,
     ContributorViewSet,
     IssueViewSet,
     CommentViewSet
)

router = DefaultRouter()
router.register(r'api/register', RegisterView, basename='register')

urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('admin/', admin.site.urls, name="admin"),

    # Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Authentication URLs
    path('api-auth/', include('rest_framework.urls')),

    # User URLs
    path('api/users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('api/users/<int:id>/', CustomUserViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user'),

    # Project URLs
    path('api/projects/', ProjectListViewSet.as_view({'get': 'list', 'post': 'create'}), name='projects'),
    path('api/projects/<str:project_id>/', ProjectDetailViewSet.as_view({
         'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project'),

    # Contributor URLs
    path('api/projects/<str:project_id>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}), name='contributors'),
    path('api/projects/<str:project_id>/contributors/<int:contributor_id>/',
         ContributorViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='contributor'),

    # Issue URLs
    path('api/projects/<str:project_id>/issues/',
         IssueViewSet.as_view({'get': 'list', 'post': 'create'}), name='issues'),
    path('api/projects/<str:project_id>/issues/<int:issue_id>/', IssueViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='issue'),

    # Comment URLs
    path('api/projects/<str:project_id>/issues/<int:issue_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('api/projects/<str:project_id>/issues/<int:issue_id>/comments/<str:comment_id>/', CommentViewSet.as_view({
         'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment'),

    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

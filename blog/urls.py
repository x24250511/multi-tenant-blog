from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PostViewSet, CommentViewSet, TenantViewSet, home, create_post, view_post, my_posts

router = DefaultRouter()
router.register(r'api/tenants', TenantViewSet)
router.register(r'api/posts', PostViewSet)
router.register(r'api/comments', CommentViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('register-tenant/', views.register_tenant, name='register_tenant'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:post_id>/', view_post, name='view_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('', include(router.urls)),  # API
]

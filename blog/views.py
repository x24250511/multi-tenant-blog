from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tenant, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from rest_framework import viewsets, permissions
from .serializers import PostSerializer, TenantSerializer, CommentSerializer
from blog.models import Tenant, TenantUser


def home(request):
    posts = Post.objects.filter(tenant=request.tenant).order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})


def register_tenant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_tenant')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_tenant')

        # create user
        user = User.objects.create_user(username=username, password=password)

        # link user to tenant
        TenantUser.objects.create(tenant=request.tenant, user=user)

        # log them automatically
        login(request, user)
        messages.success(request, f"WELCOME TO {request.tenant.name}!")
        return redirect('home')

    return render(request, 'registration/register.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(
            tenant=request.tenant,
            author=request.user,
            title=title,
            content=content
        )
        return redirect('home')
    return render(request, 'blog/create_post.html')


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, tenant=request.tenant)
    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text', '').strip()
            if text:
                Comment.objects.create(
                    tenant=request.tenant,
                    post=post,
                    author=request.user,
                    text=request.POST.get('text').strip()
                )
            return redirect('view_post', post_id=post.id)
        else:
            return redirect('login')

    comments = post.comment_set.all().order_by('-created_at')
    return render(request, 'blog/view_post.html', {'post': post, 'comments': comments})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_post.html', {'posts': posts})


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

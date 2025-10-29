from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    theme_color = models.CharField(
        max_length=20,
        default="#4f46e5",
        help_text="Hex color code for tenant theme")

    def __str__(self):
        return self.name


class TenantUser(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} @ {self.tenant.name}"


class Post(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.tenant.name})"


class Comment(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # comments = post.comment_set.filter(post__tenant=request.tenant)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

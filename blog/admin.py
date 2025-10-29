from django.contrib import admin
from .models import Tenant, Post, Comment


# Register your models here.
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'theme_color')
    search_fields = ('name', 'domain')


admin.site.register(Post)
admin.site.register(Comment)

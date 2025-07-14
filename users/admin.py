from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active']
    ordering = ['-date_joined']

admin.site.register(User, UserAdmin)

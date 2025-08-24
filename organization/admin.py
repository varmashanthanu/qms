from django.contrib import admin
from .models import Branch

# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']

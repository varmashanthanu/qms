from django.contrib import admin
from .models import KioskKey

# Register your models here.
@admin.register(KioskKey)
class KioskKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'branch', 'created_at', 'updated_at', 'used')
    search_fields = ('key', 'branch__name')
    list_filter = ('used', 'branch')
    readonly_fields = ('created_at', 'updated_at', 'key')

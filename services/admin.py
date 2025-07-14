from django.contrib import admin
from .models import Service, Category, Branch, ServiceCounter, Ticket

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(ServiceCounter)
class ServiceCounterAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'assigned_staff', 'is_active']
    search_fields = ['name', 'branch__name']
    list_filter = ['is_active', 'branch']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number', 'service', 'branch', 'status',
        'assigned_to', 'counter', 'customer_name',
        'customer_phone', 'customer_email', 'created_at'
    ]
    search_fields = ['ticket_number', 'customer_name', 'customer_phone']
    list_filter = ['status', 'branch', 'service']
    readonly_fields = ['created_at', 'called_at', 'served_at', 'completed_at']
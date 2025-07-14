"""
Custom class to manage user permissions.
"""

from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)

class IsStaff(BasePermission):
    """
    Allows access only to users with the 'staff' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'staff' or request.user.is_superuser)
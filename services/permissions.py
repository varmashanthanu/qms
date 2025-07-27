from rest_framework.permissions import BasePermission


class IsKioskToken(BasePermission):
    """
    Custom permission to only allow access to users with a valid kiosk token.
    """

    def has_permission(self, request, view):
        # Check if the request has a valid kiosk token
        token = request.auth
        if not token:
            return False

        return request.auth.get('scope') == 'kiosk'

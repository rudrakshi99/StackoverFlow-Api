from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """Permissions for logged in users"""

    def has_object_permission(self, request, view, obj):
        """Checks user permission"""
        return obj.user.id == request.user.id

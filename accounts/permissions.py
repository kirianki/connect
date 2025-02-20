from rest_framework import permissions

class IsOverallAdmin(permissions.BasePermission):
    """
    Custom permission to allow only overall admins to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'overall_admin'

class IsSectorAdmin(permissions.BasePermission):
    """
    Custom permission to allow only sector admins to manage their own sector.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sector_admin'

class IsServiceProvider(permissions.BasePermission):
    """
    Custom permission to allow only service providers to manage their profiles.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'service_provider'

class IsClient(permissions.BasePermission):
    """
    Custom permission to allow only clients to leave reviews.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'

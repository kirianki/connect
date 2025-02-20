import logging
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()
logger = logging.getLogger(__name__)

class IsOverallAdmin(permissions.BasePermission):
    """
    Custom permission to allow only overall admins to access certain views.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.debug(f"User: {request.user.username}, Role: {request.user.role}")
            return request.user.role == User.ROLE_OVERALL_ADMIN
        return False

class IsSectorAdmin(permissions.BasePermission):
    """
    Custom permission to allow only sector admins to manage their own sector.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SECTOR_ADMIN

class IsServiceProvider(permissions.BasePermission):
    """
    Custom permission to allow only service providers to manage their profiles.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SERVICE_PROVIDER

class IsClient(permissions.BasePermission):
    """
    Custom permission to allow only clients to leave reviews.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CLIENT

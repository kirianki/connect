import logging
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()
logger = logging.getLogger(__name__)

class IsOverallAdmin(permissions.BasePermission):
    """
    Allows only overall admins to access certain views.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.debug(f"User: {request.user.username}, Role: {request.user.role}")
            return request.user.role == User.Role.OVERALL_ADMIN
        return False

class IsSectorAdmin(permissions.BasePermission):
    """
    Allows only sector admins to manage their own sector.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.debug(f"User: {request.user.username}, Role: {request.user.role}")
            return request.user.role == User.Role.SECTOR_ADMIN
        return False

class IsServiceProvider(permissions.BasePermission):
    """
    Allows only service providers to manage their profiles.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.debug(f"User: {request.user.username}, Role: {request.user.role}")
            return request.user.role == User.Role.SERVICE_PROVIDER
        return False

class IsClient(permissions.BasePermission):
    """
    Allows only clients to leave reviews and make service requests.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.debug(f"User: {request.user.username}, Role: {request.user.role}")
            return request.user.role == User.Role.CLIENT
        return False

class IsOwner(permissions.BasePermission):
    """
    Ensures that only the owner of an object can edit or delete it.
    Assumes the object has an attribute 'user' or 'owner' that represents the owner.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        
        if owner and owner == request.user:
            logger.debug(f"User: {request.user.username} is the owner of object {obj}.")
            return True
        
        logger.warning(f"User: {request.user.username} tried to access unauthorized object {obj}.")
        return False

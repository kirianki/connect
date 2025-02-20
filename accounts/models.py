from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model to support different roles.
    """
    ROLE_CHOICES = (
        ('overall_admin', 'Overall Admin'),
        ('sector_admin', 'Sector Admin'),
        ('service_provider', 'Service Provider'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
